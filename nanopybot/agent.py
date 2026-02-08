import json
from .provider import ChatMessage
from .selflearn import detect_feedback

MAX_RULES = 5


class Agent:
    def __init__(self, provider, tools, memory):
        self.provider = provider
        self.tools = tools
        self.memory = memory

    async def run(self, message):
        fb = detect_feedback(message)
        if fb:
            self._remember_rule(fb)

        # 1. Check if user is manually calling a tool (e.g. from CLI)
        tool_result = self._try_run_tool(message)
        if tool_result is not None:
            return tool_result

        # 2. Start conversation
        system_prompt = self._build_system_prompt()
        history = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=message),
        ]
        
        response = await self.provider.chat(history)
        
        # 3. Check for tool calls in AI response (Dynamic Tool Invocation)
        # We allow one follow-up to summarize the tool result
        if "tool:" in response:
            for line in response.splitlines():
                if line.strip().startswith("tool:"):
                    raw_call = line.strip()
                    tool_output = self._try_run_tool(raw_call)
                    
                    # Feed the tool output back to the AI for a final summary
                    history.append(ChatMessage(role="assistant", content=response))
                    history.append(ChatMessage(role="user", content=f"[Tool Result] {tool_output}\n\nPlease summarize the result above for the user."))
                    
                    final_response = await self.provider.chat(history)
                    return f"{raw_call}\n\n{final_response}"

        return response

    def _remember_rule(self, rule):
        rules = self.memory.get("rules.list", [])
        if not isinstance(rules, list):
            rules = []

        # Keep unique order: newest first.
        rules = [rule] + [r for r in rules if r != rule]
        rules = rules[:MAX_RULES]

        self.memory.put("rules.last", rule)
        self.memory.put("rules.list", rules)

    def _build_system_prompt(self):
        rules = self.memory.get("rules.list", [])
        if not isinstance(rules, list):
            rules = []

        # List available tools for the AI to know
        tools_info = []
        for name, tool in self.tools.tools.items():
            tools_info.append(f"- {name}: {tool.description}")
        tools_str = "\n".join(tools_info)

        base = (
            "You are NanoPyBot, a self-learning AI assistant.\n"
            f"Available tools:\n{tools_str}\n\n"
            "If you need to use a tool or create a new one, output a line starting with 'tool:<name> <json_args>'.\n"
            "To create a persistent tool, use: tool:create_tool {\"name\": \"name\", \"description\": \"desc\", \"code\": \"python_body_of_run_args\"}.\n"
            "The 'code' should be the body of a 'run(args)' function, e.g., 'return args.get(\"x\") + 1'.\n"
        )
        
        if not rules:
            return base

        lines = [base, "Apply these user preferences consistently:"]
        for idx, rule in enumerate(rules, start=1):
            lines.append(f"{idx}. {rule}")
        return "\n".join(lines)

    def _try_run_tool(self, message):
        text = message.strip()
        if not text.startswith("tool:"):
            return None

        payload = text[5:].strip()
        if not payload:
            return "Invalid tool call. Use: tool:<name> [json_args]"

        parts = payload.split(None, 1)
        name = parts[0]
        raw_args = parts[1] if len(parts) > 1 else "{}"

        if not self.tools.has(name):
            return f"Unknown tool '{name}'."

        try:
            args = {} if not raw_args else json.loads(raw_args)
        except Exception:
            return "Invalid tool args. Provide valid JSON object."
        if not isinstance(args, dict):
            return "Invalid tool args. JSON args must be an object."

        try:
            result = self.tools.call(name, args)
            return f"[tool:{name}] {result}"
        except Exception as e:
            return f"Tool '{name}' failed: {e}"
