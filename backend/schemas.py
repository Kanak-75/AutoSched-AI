from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class MeetingMode(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class MeetingApp(str, Enum):
    MEET = "meet"
    ZOOM = "zoom"
    TEAMS = "teams"


class ScheduleRequest(BaseModel):
    """
    Single, central Pydantic schema used as the JSON contract between:
    - Frontend → Backend
    - Backend → Gemini (prompt/response)
    - Backend → Persistence / Scheduler
    - Scheduler → Email template
    """

    title: str = Field(..., description="Short title for the event.")
    description: Optional[str] = None

    mode: Optional[MeetingMode] = Field(
        None,
        description=(
            "Optional meeting mode. If 'online', app/link should be set. "
            "If 'offline', location should be set."
        ),
    )

    application: Optional[MeetingApp] = Field(
        None,
        description="Online meeting application (Meet / Zoom / Teams) when mode=online.",
    )
    meeting_link: Optional[HttpUrl] = None

    location: Optional[str] = None

    # Core datetime fields in UTC
    start_time_utc: datetime = Field(..., description="Event start time in UTC.")
    end_time_utc: Optional[datetime] = None

    # User timezone for display, e.g. "Asia/Kolkata"
    timezone: str = Field(..., description="IANA timezone name for the user.")

    # Reminder configuration (multi-reminder support)
    reminder_minutes_before: int = Field(
        15, description="Minutes before meeting to send the first reminder."
    )
    reminder_count: int = Field(
        1, description="How many reminders to send in total (>=1)."
    )
    reminder_interval_minutes: int = Field(
        5,
        description=(
            "Minutes between repeated reminders when reminder_count > 1. "
            "Ignored when reminder_count == 1."
        ),
    )

    # Optional cron for recurring reminders
    cron_expression: Optional[str] = Field(
        None,
        description=(
            "Optional cron expression for recurring reminders. "
            "Used to create APScheduler Cron jobs."
        ),
    )

    email_to: str = Field(..., description="Recipient email address for reminders.")

    json_created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Auto timestamp when this JSON payload was created (UTC).",
    )

    class Config:
        from_attributes = True


