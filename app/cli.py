import typer, asyncio, json, time
from rich.console import Console
from .config import load_config
from .provider import OpenAICompatProvider, ProviderError
from .memory import MemoryStore
from .tools import default_tools
from .agent import Agent
from .scheduler import build_scheduler, parse_cron

app = typer.Typer()
console = Console()

def build_agent():
    cfg = load_config()
    p = cfg.provider
    return Agent(
        OpenAICompatProvider(p.api_key, p.base_url, p.model),
        default_tools(),
        MemoryStore(cfg.memory_path),
    )

@app.command()
def agent(message: str):
    try:
        console.print(asyncio.run(build_agent().run(message)))
    except ProviderError as e:
        console.print(f"[red]Provider error:[/red] {e}")

@app.command()
def cron_add(name: str, message: str, cron: str):
    cfg = load_config()
    s = build_scheduler(cfg.scheduler_db)
    s.start(paused=True)
    s.add_job(
        "nanopybot.cron_runner:run_agent_job",
        parse_cron(cron),
        id=name,
        kwargs={"payload_json": json.dumps({"message": message})},
        replace_existing=True,
    )
    s.shutdown()
    console.print(f"Added cron {name}")

@app.command()
def cron_run():
    cfg = load_config()
    s = build_scheduler(cfg.scheduler_db)
    s.start()
    console.print("Scheduler running")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        s.shutdown()
