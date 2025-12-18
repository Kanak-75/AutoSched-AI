from __future__ import annotations

import json
import os
from typing import Any, Dict

from pydantic import ValidationError

from .schemas import ScheduleRequest

try:
    # Optional import; you must install `google-genai` and set GEMINI_API_KEY
    from google import genai

    _gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
except Exception:  # pragma: no cover - optional dependency
    _gemini_client = None


_SCHEMA_EXAMPLE: Dict[str, Any] = {
    "title": "Project Kickoff",
    "description": "Kickoff with team.",
    "mode": "online",
    "application": "meet",
    "meeting_link": "https://meet.google.com/xyz-abc",
    "location": None,
    "start_time_utc": "2025-12-20T11:30:00Z",
    "end_time_utc": None,
    "timezone": "Asia/Kolkata",
    "reminder_minutes_before": 30,
    "reminder_count": 2,
    "reminder_interval_minutes": 10,
    "cron_expression": None,
    "email_to": "user@example.com",
    "json_created_at": "2025-12-18T09:00:00Z",
}


def call_gemini_and_validate(natural_text: str) -> ScheduleRequest:
    """
    Call the Gemini multimodal LLM and force structured JSON output
    that conforms to the single Pydantic schema `ScheduleRequest`.

    For local testing without Gemini, you can instead send a JSON string
    that already matches the schema and use `validate_gemini_json`.
    """
    if _gemini_client is None:
        # Fallback: expect natural_text to be a JSON string for local dev.
        return validate_gemini_json(natural_text)

    prompt = f"""
You are a scheduling assistant. Read the user request and respond with ONLY a JSON object
that matches this example schema (no extra text, no markdown):

{json.dumps(_SCHEMA_EXAMPLE, indent=2)}

Rules:
- All datetime fields must be ISO 8601 UTC (e.g. "2025-12-20T11:30:00Z").
- `mode` must be "online" or "offline".
- `application` must be "meet", "zoom", or "teams" (or null).
- If meeting is online, include `meeting_link`.
- If meeting is offline, include `location`.
- `timezone` must be a valid IANA timezone (e.g. "Asia/Kolkata").
- `reminder_minutes_before`: integer.
- `reminder_count`: integer >= 1.
- `reminder_interval_minutes`: integer >= 1.

User input:
{natural_text}
"""

    resp = _gemini_client.models.generate_content(
        model="gemini-1.5-pro",
        contents=[prompt],
        config={"response_mime_type": "application/json"},
    )
    raw = resp.text
    return validate_gemini_json(raw)


def validate_gemini_json(raw_json: str | Dict[str, Any]) -> ScheduleRequest:
    """
    Helper that takes JSON from Gemini (string or dict) and validates it
    against the single Pydantic schema.
    """
    if isinstance(raw_json, str):
        data = json.loads(raw_json)
    else:
        data = raw_json

    try:
        return ScheduleRequest(**data)
    except ValidationError as exc:
        raise exc

