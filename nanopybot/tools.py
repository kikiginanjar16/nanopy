import importlib.util
import os
from pathlib import Path

class Tool:
    def __init__(self, name, description, fn):
        self.name = name
        self.description = description
        self.fn = fn

class ToolRegistry:
    def __init__(self, custom_path=None, config=None):
        self.tools = {}
        self.config = config
        self.custom_path = Path(custom_path) if custom_path else None
        if self.custom_path:
            self.custom_path.mkdir(parents=True, exist_ok=True)
            self._load_custom()

    def register(self, tool):
        self.tools[tool.name] = tool

    def call(self, name, args):
        # Pass config as second argument if the tool supports it
        import inspect
        fn = self.tools[name].fn
        sig = inspect.signature(fn)
        if len(sig.parameters) >= 2:
            return fn(args, self.config)
        return fn(args)

    def has(self, name):
        return name in self.tools

    def _load_custom(self):
        for file in self.custom_path.glob("*.py"):
            name = file.stem
            spec = importlib.util.spec_from_file_location(name, file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "run"):
                desc = getattr(mod, "DESCRIPTION", "Custom tool")
                self.register(Tool(name, desc, mod.run))

    def add_custom(self, name, description, code):
        if not self.custom_path:
            return "No custom tool path configured."
        
        file_path = self.custom_path / f"{name}.py"
        
        # Clean up the code
        import re
        clean_lines = []
        for line in code.splitlines():
            # Skip signature lines and markdown markers
            l = line.strip()
            if l.startswith("```"): continue
            if l.startswith("def run"): continue
            clean_lines.append(line) # Keep original indentation if possible
        
        clean_code = "\n".join(clean_lines).strip()
        
        # Ensure the body is indented correctly for the template
        final_lines = []
        for line in clean_code.splitlines():
            if not line.startswith("    ") and not line.startswith("\t"):
                final_lines.append(f"    {line}")
            else:
                final_lines.append(line)
        
        indented_code = "\n".join(final_lines)
        full_code = f'DESCRIPTION = "{description}"\n\ndef run(args):\n{indented_code}'
            
        file_path.write_text(full_code, encoding="utf-8")
        
        # Reload to make it available
        spec = importlib.util.spec_from_file_location(name, file_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.register(Tool(name, description, mod.run))
        return f"Tool '{name}' added successfully."

def default_tools(custom_path=None, config=None):
    reg = ToolRegistry(custom_path, config)
    
    def get_time(_):
        import time
        t = time.time()
        return {
            "unix": t,
            "local": time.ctime(t),
            "timezone": time.tzname[0]
        }
    
    reg.register(Tool("time", "Get current time (unix and local)", get_time))
    
    # Built-in tool to add other tools
    def create_tool_fn(args):
        name = args.get("name")
        desc = args.get("description")
        code = args.get("code")
        if not all([name, desc, code]):
            return "Error: name, description, and code are required."
        return reg.add_custom(name, desc, code)

    reg.register(Tool("create_tool", "Create a new custom tool. Args: {name, description, code (python snippet for run(args) body)}", create_tool_fn))
    
    return reg
