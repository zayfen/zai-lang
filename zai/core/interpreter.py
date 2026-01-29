import re
import os
import json
import time
import uuid
from .environment import Environment
from ..runtime.bridge import AIBridge, ExecBridge
from ..runtime.default_bridge import DefaultAIBridge, DefaultExecBridge

class Interpreter:
    def __init__(self, tree, ai_bridge=None, exec_bridge=None, base_path=".", wait_timeout=60, source_file=None):
        self.tree = tree
        self.env = Environment()
        self.skills = {}
        self.agent_name = ""
        self.persona = {}
        self.ai_bridge = ai_bridge or DefaultAIBridge()
        self.exec_bridge = exec_bridge or DefaultExecBridge()
        self.base_path = base_path
        self.imported_files = set()  # prevent circular imports
        self.ipc_root = os.path.join(os.getcwd(), ".zai_ipc")
        self.wait_timeout = wait_timeout
        self.source_file = source_file

    def _ensure_ipc_dir(self, agent_name):
        path = os.path.join(self.ipc_root, agent_name)
        os.makedirs(path, exist_ok=True)
        return path

    def resolve_template(self, template_str, env):
        if not isinstance(template_str, str): return template_str
        def replace(match):
            key = match.group(1)
            try:
                return str(env.get_var(key))
            except:
                val = self.env.get_context(key)
                return str(val if val is not None else f"{{{key}}}")
        return re.sub(r"\{([a-zA-Z0-9_]+)\}", replace, template_str)

    def visit(self, node, env):
        if node is None: return None
        if not hasattr(node, 'data'): 
            return self.evaluate(node, env)
        method_name = f'visit_{node.data}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, env)

    def generic_visit(self, node, env):
        last_result = None
        for child in node.children:
            if child is not None:
                last_result = self.visit(child, env)
                if isinstance(last_result, dict) and (last_result.get("final") or last_result.get("status") == "fail"):
                    return last_result
        return last_result

    def run(self, agent_name=None, entry_skill="Main", entry_args=None):
        root = self.tree
        if root.data == 'start':
            target_agent = None
            if agent_name:
                for child in root.children:
                    if hasattr(child, 'data') and child.data == 'agent' and child.children[0].value == agent_name:
                        target_agent = child
                        break
                if not target_agent:
                    raise ValueError(f"Agent '{agent_name}' not found")
            else:
                # Default to first agent
                for child in root.children:
                    if hasattr(child, 'data') and child.data == 'agent':
                        target_agent = child
                        break
                if not target_agent:
                    # Could be just config file
                    return {}
            root = target_agent
        
        if root.data == 'agent':
            self.agent_name = root.children[0].value
            self.context_defined = False
            
            for agent_child in root.children[1:]:
                if not hasattr(agent_child, 'data'): continue
                if agent_child.data == 'context_def':
                    self.visit_context_def(agent_child, self.env)
                elif agent_child.data == 'import_stmt':
                    self.visit_import_stmt(agent_child, self.env)
                elif agent_child.data == 'persona_def':
                    self.visit_persona_def(agent_child, self.env)
                elif agent_child.data == 'skill_def':
                    name = agent_child.children[0].value
                    self.skills[name] = agent_child
 
        return self.execute_skill(entry_skill, entry_args or {})

    def visit_context_def(self, node, env):
        if self.context_defined:
            raise RuntimeError("Multiple context definitions found. An agent can only have one context.")
        self.context_defined = True
        
        for item in node.children:
            if hasattr(item, 'data') and item.data == 'context_item':
                key = item.children[0].value
                val = self.evaluate(item.children[1], env)
                self.env.set_context(key, val)

    def visit_import_stmt(self, node, env):
        from .parser import get_parser
        rel_path = self.evaluate(node.children[0], env)
        abs_path = os.path.abspath(os.path.join(self.base_path, rel_path))
        
        if abs_path in self.imported_files:
            return # Skip already imported file
            
        self.imported_files.add(abs_path)
        
        if not os.path.exists(abs_path):
             print(f"Warning: Import file not found: {abs_path}")
             return

        with open(abs_path, 'r') as f:
            code = f.read()
            
        parser = get_parser()
        tree = parser.parse(code, start='config_file')
        
        # We need to process definitions in the imported file
        # imports in imports are also possible, so recursive visit is good
        # but we need to ensure we don't reset scope incorrectly.
        # config_file children are context_def or persona_def.
        for child in tree.children:
            self.visit(child, env)

    def visit_persona_def(self, node, env):
        name = node.children[0].value
        if name not in self.persona:
            self.persona[name] = {}
        for item in node.children[1:]:
            if hasattr(item, 'data') and item.data == 'persona_item':
                key = item.children[0].value
                # Store the AST node (either expression or persona_block)
                self.persona[name][key] = item.children[1]

    def visit_persona_block(self, node, env):
        fragments = []
        for fragment in node.children:
            val = self.visit(fragment, env)
            if val: fragments.append(str(val))
        return " ".join(fragments)

    def visit_persona_if(self, node, env):
        cond = self.evaluate(node.children[0], env)
        if cond:
            return self.visit(node.children[1], env)
        elif len(node.children) > 2 and node.children[2] is not None:
            return self.visit(node.children[2], env)
        return ""

    def evaluate_persona(self, persona_name, key, env):
        if persona_name not in self.persona: return ""
        node = self.persona[persona_name].get(key)
        if node is None: return ""
        
        # If it was an inline expression (not a block)
        if not hasattr(node, 'data') or node.data != 'persona_block':
            val = self.evaluate(node, env)
            return self.resolve_template(val, env)
        
        # If it is a block
        val = self.visit(node, env)
        return self.resolve_template(val, env)

    def execute_skill(self, name, args):
        if name not in self.skills:
            return {"status": "fail", "code": 404, "message": f"Skill '{name}' not found"}
        
        skill_node = self.skills[name]
        body_start_index = 2
        
        local_env = Environment(parent=self.env)
        for k, v in args.items():
            self.env.set_context(k, v)

        for stmt in skill_node.children[body_start_index:]:
            if not hasattr(stmt, 'data'): continue
            result = self.visit(stmt, local_env)
            if isinstance(result, dict) and (result.get("final") or result.get("status") == "fail"):
                return result
        return {"status": "success", "code": 0, "message": "OK", "final": True}

    def visit_var_decl(self, node, env):
        name = node.children[0].value
        val = self.evaluate(node.children[1], env)
        env.set_var(name, val)

    def visit_assignment(self, node, env):
        target_node = node.children[0]
        val = self.evaluate(node.children[1], env)
        if hasattr(target_node, 'data') and target_node.data == 'context_var':
            key = target_node.children[1].value 
            self.env.set_context(key, val)
        else:
            env.set_var(target_node.value, val)

    def visit_if_stmt(self, node, env):
        cond = self.evaluate(node.children[0], env)
        if cond:
            return self.visit(node.children[1], env)
        elif len(node.children) > 2 and node.children[2] is not None:
            return self.visit(node.children[2], env)

    def visit_while_stmt(self, node, env):
        while self.evaluate(node.children[0], env):
            result = self.visit(node.children[1], env)
            if isinstance(result, dict) and (result.get("final") or result.get("status") == "fail"):
                return result

    def visit_block(self, node, env):
        last_result = None
        for stmt in node.children:
            if hasattr(stmt, 'data'):
                last_result = self.visit(stmt, env)
                if isinstance(last_result, dict) and (last_result.get("final") or last_result.get("status") == "fail"):
                    return last_result
        return last_result

    def visit_response_stmt(self, node, env):
        val = self.evaluate(node.children[0], env)
        msg = self.resolve_template(val, env)
        print(f"[{self.agent_name}] Agent: {msg}")

    def visit_ask_stmt(self, node, env):
        prompt = self.evaluate(node.children[0], env)
        match = re.search(r"\{([a-zA-Z0-9_]+)=\}", prompt)
        if match:
            var_name = match.group(1)
            clean_prompt = prompt.replace(f"{{{var_name}=}}", "").strip()
            user_val = input(f"[{self.agent_name}] {clean_prompt} ")
            self.env.set_context(var_name, user_val)
        else:
            input(f"[{self.agent_name}] {prompt} ")

    def visit_process_stmt(self, node, env):
        prompt = self.evaluate(node.children[0], env)
        keys = [self.evaluate(tok, env) for tok in node.children[1:] if tok is not None]
        
        # STRICT PERSONA BINDING: Merge all available personas
        full_system_prompt = []
        for persona_name in self.persona:
            if 'base_instruction' in self.persona[persona_name]:
                 instruction = self.evaluate_persona(persona_name, 'base_instruction', env)
                 if instruction:
                     full_system_prompt.append(f"--- Persona: {persona_name} ---\n{instruction}\n")
        
        system = "\n".join(full_system_prompt)
        res = self.ai_bridge.handle(prompt, keys, system, self.env.context)
        for k, v in res.items(): self.env.set_context(k, v)

    def visit_exec_stmt(self, node, env):
        cmd = self.evaluate(node.children[0], env)
        keys = [self.evaluate(tok, env) for tok in node.children[1:] if tok is not None]
        res = self.exec_bridge.handle(cmd, keys)
        for k, v in res.items(): self.env.set_context(k, v)

    def visit_notify_stmt(self, node, env):
        target_agent = node.children[0].value
        cmd_type = self.evaluate(node.children[1], env)
        payload = self.evaluate(node.children[2], env)
        
        # Write to target agent's IPC directory
        target_dir = self._ensure_ipc_dir(target_agent)
        message = {
            "source": self.agent_name,
            "type": cmd_type,
            "payload": payload,
            "timestamp": time.time()
        }
        
        filename = f"{uuid.uuid4()}.json"
        with open(os.path.join(target_dir, filename), "w") as f:
            json.dump(message, f)
            
        print(f"[{self.agent_name}] Notified {target_agent}: {cmd_type}")

    def visit_wait_stmt(self, node, env):
        code_var = node.children[0].value
        msg_var = node.children[1].value
        target_source = node.children[2].value # We expect this to be the source agent name
        
        my_dir = self._ensure_ipc_dir(self.agent_name)
        
        print(f"[{self.agent_name}] Waiting for signal from {target_source}...")
        
        # Simple polling loop
        timeout = self.wait_timeout 
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            found_msg = None
            found_file = None
            
            # Check for messages
            if os.path.exists(my_dir):
                files = os.listdir(my_dir)
                for fname in files:
                    if not fname.endswith(".json"): continue
                    fpath = os.path.join(my_dir, fname)
                    try:
                        with open(fpath, 'r') as f:
                            msg = json.load(f)
                            
                        # Check if message is from the expected source
                        if msg.get("source") == target_source:
                            found_msg = msg
                            found_file = fpath
                            break
                    except:
                        pass
            
            if found_msg:
                # Consume message
                os.remove(found_file)
                env.set_var(code_var, found_msg.get("type")) # usually numeric code or string
                env.set_var(msg_var, found_msg.get("payload"))
                return
            
            time.sleep(0.5)
            
        # Timeout case
        print(f"[{self.agent_name}] Wait timed out!")
        env.set_var(code_var, -1)
        env.set_var(msg_var, "TIMEOUT")

    def visit_template_render(self, node, env):
        tpl_str = env.get_var(node.children[0].value)
        temp_ctx = self.env.context.copy()
        if len(node.children) > 1:
            for assign in node.children[1].children:
                 temp_ctx[assign.children[0].value] = self.evaluate(assign.children[1], env)
        return self.resolve_template(tpl_str, temp_ctx)

    def visit_skill_invoke(self, node, env):
        name = node.children[0].value
        call_args = {}
        if len(node.children) > 1 and node.children[1] is not None:
            for assign in node.children[1].children:
                call_args[assign.children[0].value] = self.evaluate(assign.children[1], env)
        res = self.execute_skill(name, call_args)
        if isinstance(res, dict) and res.get("status") == "success":
            res["final"] = False
        return res

    def visit_success_stmt(self, node, env):
        return {"status": "success", "code": int(self.evaluate(node.children[0], env)), "message": self.evaluate(node.children[1], env), "final": True}

    def visit_start_stmt(self, node, env):
        target_agent = node.children[0].value
        print(f"[{self.agent_name}] Starting sub-agent: {target_agent}")
        
        import subprocess
        import sys
        
        # If we have the source file, we can spawn a new process
        if self.source_file:
             cmd = [sys.executable, "-m", "zai.cli", self.source_file, "--agent", target_agent]
             # Run in background? The user said "child agent... can execute wait notify"
             # Ideally this should be non-blocking or managed. 
             # "start" usually implies async spawning.
             subprocess.Popen(cmd)
        else:
             print("Warning: Cannot start agent, source file not known.")

    def visit_fail_stmt(self, node, env):
        return {"status": "fail", "code": int(self.evaluate(node.children[0], env)), "message": self.evaluate(node.children[1], env), "final": True}

    def evaluate(self, node, env):
        if node is None: return None
        if not hasattr(node, 'data'):
            if hasattr(node, 'type'):
                if node.type == 'ESCAPED_STRING': return node.value[1:-1]
                if node.type == 'MULTILINE_STRING': return node.value[3:-3]
                if node.type == 'SIGNED_NUMBER': return float(node.value)
                if node.type == 'IDENTIFIER':
                    try: return env.get_var(node.value)
                    except: return self.env.get_context(node.value)
            return node
        
        if node.data == 'true': return True
        if node.data == 'false': return False
        
        if node.data in ['string', 'number', 'simple_expression', 'expression', 'boolean']: 
            return self.evaluate(node.children[0], env)
        if node.data == 'template_render': return self.visit_template_render(node, env)
        if node.data == 'context_var': return self.env.get_context(node.children[1].value)
        if node.data == 'persona_ref':
            persona_name = node.children[0].value
            item_key = node.children[1].value
            return self.evaluate_persona(persona_name, item_key, env)
        if node.data == 'binary_op':
            l, op, r = self.evaluate(node.children[0], env), node.children[1].value, self.evaluate(node.children[2], env)
            if l is None: l = 0
            if r is None: r = 0
            try:
                if op == '+': return (l + r) if isinstance(l, (int, float)) else (str(l) + str(r))
                if op == '-': return float(l) - float(r)
                if op == '*': return float(l) * float(r)
                if op == '/': return float(l) / float(r)
                if op == '==': return str(l) == str(r)
                if op == '!=': return str(l) != str(r)
                if op == '>': return float(l) > float(r)
                if op == '<': return float(l) < float(r)
                if op == '>=': return float(l) >= float(r)
                if op == '<=': return float(l) <= float(r)
                if op == '&&': return bool(l) and bool(r)
                if op == '||': return bool(l) or bool(r)
            except: return False
        return None
