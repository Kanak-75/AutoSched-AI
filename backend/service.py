from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from .llm_client import call_gemini_and_validate
from .schemas import ScheduleRequest
from .scheduler import schedule_jobs_for_request


def handle_natural_language_request(
    natural_text: str,
    scheduler: BackgroundScheduler,
) -> ScheduleRequest:
    """
    End-to-end backend flow for a scheduling request:

    - Take natural language text from the frontend
    - Call Gemini and validate JSON into a single Pydantic schema
    - Optionally persist to Postgres (not implemented here)
    - Register APScheduler jobs (date + cron)
    - Return the validated schema back to the caller
    """
    schedule = call_gemini_and_validate(natural_text)

    # TODO: optional persistence to PostgreSQL goes here.
    # e.g. map `ScheduleRequest` to a Django model and save.

    schedule_jobs_for_request(scheduler, schedule)

    return schedule


