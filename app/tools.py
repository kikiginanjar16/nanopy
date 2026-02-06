class Tool:
    def __init__(self, name, description, fn):
        self.name = name
        self.description = description
        self.fn = fn

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def call(self, name, args):
        return self.tools[name].fn(args)

    def has(self, name):
        return name in self.tools

def default_tools():
    reg = ToolRegistry()
    reg.register(Tool("time", "Get unix time", lambda _: __import__("time").time()))
    return reg
