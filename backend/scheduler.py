from __future__ import annotations

from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Optional
from zoneinfo import ZoneInfo

import smtplib
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

from .schemas import ScheduleRequest


def _build_email(schedule: ScheduleRequest) -> EmailMessage:
    """
    Designated email format for meeting reminders.
    """
    msg = EmailMessage()
    msg["Subject"] = f"[AutoSched] Reminder: {schedule.title}"
    msg["To"] = schedule.email_to
    msg["From"] = "no-reply@autosched-ai.local"

    user_tz = ZoneInfo(schedule.timezone)
    start_local = schedule.start_time_utc.replace(tzinfo=ZoneInfo("UTC")).astimezone(
        user_tz
    )

    body_lines = [
        "Hello,",
        "",
        f"This is a reminder for your meeting: {schedule.title}",
        f"Date & time ({schedule.timezone}): {start_local.strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Mode: {schedule.mode.value if schedule.mode else 'N/A'}",
    ]

    if schedule.application:
        body_lines.append(f"Platform: {schedule.application.value}")
    if schedule.meeting_link:
        body_lines.append(f"Meeting URL: {schedule.meeting_link}")
    if schedule.location:
        body_lines.append(f"Location: {schedule.location}")
    if schedule.description:
        body_lines.extend(["", "Details:", schedule.description])

    body_lines.extend(["", "This email was sent by AutoSched-AI."])

    msg.set_content("\n".join(body_lines))
    return msg


def send_email_via_smtp(msg: EmailMessage) -> None:
    """
    Low-level SMTP email trigger.

    Configure host, port, and credentials via environment variables or
    your Django settings and wire them in here.
    """
    host = "localhost"
    port = 25

    with smtplib.SMTP(host, port) as server:
        server.send_message(msg)


def reminder_job(schedule: ScheduleRequest) -> None:
    """
    APScheduler job function that sends the reminder email.
    """
    email = _build_email(schedule)
    send_email_via_smtp(email)


def schedule_jobs_for_request(
    scheduler: BackgroundScheduler, schedule: ScheduleRequest
) -> None:
    """
    Creates multiple APScheduler jobs (date + optional cron) based on a single
    `ScheduleRequest` instance.
    """
    # Multi reminder logic: first reminder X minutes before, then repeated.
    first_run = schedule.start_time_utc - timedelta(
        minutes=schedule.reminder_minutes_before
    )

    for i in range(schedule.reminder_count):
        run_time = first_run + timedelta(
            minutes=i * schedule.reminder_interval_minutes
        )
        trigger = DateTrigger(run_date=run_time)
        scheduler.add_job(
            reminder_job,
            trigger=trigger,
            args=[schedule],
            id=f"reminder-{schedule.json_created_at.isoformat()}-{i}",
            replace_existing=False,
        )

    # Recurring reminders (CronTrigger) if specified
    if schedule.cron_expression:
        parts = schedule.cron_expression.split()
        if len(parts) != 5:
            raise ValueError(f"Invalid cron expression: {schedule.cron_expression}")

        minute, hour, day, month, day_of_week = parts
        trigger = CronTrigger(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
            timezone=ZoneInfo("UTC"),
        )

        scheduler.add_job(
            reminder_job,
            trigger=trigger,
            args=[schedule],
            id=f"reminder-cron-{schedule.json_created_at.isoformat()}",
            replace_existing=True,
        )


def create_scheduler() -> BackgroundScheduler:
    """
    Factory for a shared BackgroundScheduler instance.

    In Django you would typically call this from AppConfig.ready()
    and keep the scheduler globally accessible.
    """
    scheduler = BackgroundScheduler(timezone=ZoneInfo("UTC"))
    scheduler.start()
    return scheduler


