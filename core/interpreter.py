import re
import json
import requests
import subprocess
import os
import sys

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.context = {}
        self.parent = parent

    def get_var(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_var(name)
        raise NameError(f"Variable '{name}' not found")

    def set_var(self, name, value):
        self.variables[name] = value

    def get_context(self, name):
        if name in self.context:
            return self.context[name]
        if self.parent:
            return self.parent.get_context(name)
        return None

    def set_context(self, name, value):
        self.context[name] = value

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.env = Environment()
        self.tasks = {}
        self.job_name = ""
        self.conversion = {}

    def resolve_template(self, template_str, context):
        if not isinstance(template_str, str): return template_str
        def replace(match):
            key = match.group(1)
            return str(context.get(key, f"{{{key}}}"))
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

    def run(self, entry_task="Main", entry_args=None):
        root = self.tree
        if root.data == 'start':
            root = next(child for child in root.children if hasattr(child, 'data') and child.data == 'job')
        
        if root.data == 'job':
            self.job_name = root.children[0].value
            for job_child in root.children[1:]:
                if not hasattr(job_child, 'data'): continue
                if job_child.data == 'context_def':
                    self.visit_context_def(job_child, self.env)
                elif job_child.data == 'conversion_def':
                    self.visit_conversion_def(job_child, self.env)
                elif job_child.data == 'task_def':
                    name = job_child.children[0].value
                    self.tasks[name] = job_child

        return self.execute_task(entry_task, entry_args or {})

    def visit_context_def(self, node, env):
        for item in node.children:
            if hasattr(item, 'data') and item.data == 'context_item':
                key = item.children[0].value
                val = self.evaluate(item.children[1], env)
                self.env.set_context(key, val)

    def visit_conversion_def(self, node, env):
        for item in node.children:
            if hasattr(item, 'data') and item.data == 'conversion_item':
                key = item.children[0].value
                val = self.evaluate(item.children[1], env)
                self.conversion[key] = val

    def execute_task(self, name, args):
        if name not in self.tasks:
            return {"status": "fail", "code": 404, "message": f"Task '{name}' not found"}
        
        task_node = self.tasks[name]
        body_start_index = 2
        
        local_env = Environment(parent=self.env)
        for k, v in args.items():
            self.env.set_context(k, v)

        for stmt in task_node.children[body_start_index:]:
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
        msg = self.resolve_template(val, self.env.context)
        print(f"[{self.job_name}] Agent: {msg}")

    def visit_ask_stmt(self, node, env):
        prompt = self.evaluate(node.children[0], env)
        match = re.search(r"\{([a-zA-Z0-9_]+)=\}", prompt)
        if match:
            var_name = match.group(1)
            clean_prompt = prompt.replace(f"{{{var_name}=}}", "").strip()
            user_val = input(f"[{self.job_name}] {clean_prompt} ")
            self.env.set_context(var_name, user_val)
        else:
            input(f"[{self.job_name}] {prompt} ")

    def visit_process_stmt(self, node, env):
        prompt_expr = self.evaluate(node.children[0], env)
        extract_keys = [self.evaluate(tok, env) for tok in node.children[1:] if tok is not None]
        system_prompt = self.resolve_template(self.conversion.get('base_instruction', ""), self.env.context)
        mock_data = {k: f"mock_{k}" for k in extract_keys}
        for k, v in mock_data.items(): self.env.set_context(k, v)

    def visit_exec_stmt(self, node, env):
        cmd = self.evaluate(node.children[0], env)
        filter_keys = [self.evaluate(tok, env) for tok in node.children[1:] if tok is not None]
        result = {"stock_count": 10, "output": "shell result"}
        for k in filter_keys:
            if k in result: self.env.set_context(k, result[k])

    def visit_notify_stmt(self, node, env):
        pass

    def visit_wait_stmt(self, node, env):
        env.set_var(node.children[0].value, 200); env.set_var(node.children[1].value, "MOCK_SUCCESS")

    def visit_template_render(self, node, env):
        tpl_str = env.get_var(node.children[0].value)
        temp_ctx = self.env.context.copy()
        if len(node.children) > 1:
            for assign in node.children[1].children:
                 temp_ctx[assign.children[0].value] = self.evaluate(assign.children[1], env)
        return self.resolve_template(tpl_str, temp_ctx)

    def visit_task_call(self, node, env):
        name = node.children[0].value
        call_args = {}
        if len(node.children) > 1:
            for assign in node.children[1].children:
                call_args[assign.children[0].value] = self.evaluate(assign.children[1], env)
        res = self.execute_task(name, call_args)
        if isinstance(res, dict) and res.get("status") == "success":
            res["final"] = False
        return res

    def visit_success_stmt(self, node, env):
        return {"status": "success", "code": int(self.evaluate(node.children[0], env)), "message": self.evaluate(node.children[1], env), "final": True}

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
        
        if node.data in ['string', 'number', 'simple_expression', 'expression']: 
            return self.evaluate(node.children[0], env)
        if node.data == 'template_render': return self.visit_template_render(node, env)
        if node.data == 'context_var': return self.env.get_context(node.children[1].value)
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

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.parser import get_parser
    parser = get_parser()
    with open(sys.argv[1] if len(sys.argv) > 1 else 'examples/test_parser.al') as f:
        tree = parser.parse(f.read())
    Interpreter(tree).run()
