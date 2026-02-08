from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from pathlib import Path

def build_scheduler(db):
    p = Path(db)
    p.parent.mkdir(parents=True, exist_ok=True)
    return BackgroundScheduler(
        jobstores={"default": SQLAlchemyJobStore(url=f"sqlite:///{p}")}
    )

def parse_cron(expr):
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError(
            f"Invalid cron expression '{expr}'. Expected 5 fields (minute hour day month day_of_week), e.g. '0 7 * * *'."
        )

    m, h, d, mo, w = parts
    try:
        return CronTrigger(minute=m, hour=h, day=d, month=mo, day_of_week=w)
    except ValueError as e:
        raise ValueError(f"Invalid cron expression '{expr}': {e}") from e
