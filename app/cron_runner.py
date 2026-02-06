import asyncio, json
from .cli import build_agent

def run_agent_job(payload_json):
    payload = json.loads(payload_json)
    msg = payload.get("message")
    if msg:
        asyncio.run(build_agent().run(msg))