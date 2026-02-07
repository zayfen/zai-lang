import json
from openai import OpenAI
from .bridge import AIBridge, ExecBridge
from ..builtin import tools
from ..config import get_str, get_float

class DefaultAIBridge(AIBridge):
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or get_str("ZAI_API_KEY")
        self.base_url = base_url or get_str("ZAI_BASE_URL")
        self.model = get_str("ZAI_MODEL", "deepseek-reasoner")
        self.temperature = get_float("ZAI_TEMPERATURE", 0.0)
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        print(f"[DefaultAIBridge] API_KEY: {self.api_key}  ; BASE_URL: {self.base_url} ; TEMPERATURE: {self.temperature}")

    def handle(self, prompt, extract_keys, system_prompt, context):
        # print(f"[DefaultAIBridge] {prompt=} {extract_keys=} {system_prompt=} {context=}")
        # Format the context for the AI
        context_str = json.dumps(context, indent=2, ensure_ascii=False)
        full_prompt = f"Context:\n{context_str}\n\nTask: {prompt}\n\nPlease return a JSON object with the following keys: {', '.join(extract_keys)}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            response_format={"type": "json_object"}
        )

        try:
            result = json.loads(response.choices[0].message.content)
            return {k: result.get(k) for k in extract_keys}
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"ERROR: Failed to parse AI response: {e}")
            return {k: None for k in extract_keys}

class DefaultExecBridge(ExecBridge):
    def handle(self, cmd, filter_keys):
        # cmd is expected to be a string or a dict-like structured command
        # For simple string commands, we use the bash tool.
        # But for structured commands (not yet fully defined in EBNF but used in thought),
        # we might want to route to specific tools.
        
        # Heuristic: if it looks like a bash command, use tools.bash
        # Otherwise, if we can parse it as a tool call, use that.
        
        # For now, let's treat cmd as a bash command unless it matches a builtin tool name.
        parts = cmd.split(maxsplit=1)
        tool_name = parts[0]
        args_str = parts[1] if len(parts) > 1 else ""
        
        result = {}
        if hasattr(tools, tool_name):
            # Attempt to execute as a builtin tool
            # This is a bit simplified; real Zai might pass structured args.
            # Here we assume bash-like space-separated arguments for simplicity.
            # Or if it's 'ls .', it calls tools.ls('.')
            try:
                import shlex
                args = shlex.split(args_str)
                func = getattr(tools, tool_name)
                # Call function with positional arguments
                result = func(*args)
            except Exception as e:
                result = {"error": f"Tool '{tool_name}' failed: {e}"}
        else:
            # Fallback to bash
            result = tools.bash(cmd)
            
        # Apply filter keys
        if not filter_keys:
            return result
            
        return {k: result.get(k) for k in filter_keys if k in result}
