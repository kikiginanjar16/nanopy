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

        tool_result = self._try_run_tool(message)
        if tool_result is not None:
            return tool_result

        system_prompt = self._build_system_prompt()

        msgs = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=message),
        ]
        return await self.provider.chat(msgs)

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

        base = "You are NanoPyBot."
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
