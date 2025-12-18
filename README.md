## AutoSched-AI

Centralized scheduling core with:

- **Gemini LLM** for natural language → JSON
- **Single Pydantic schema** as the contract
- **APScheduler** for multiple jobs / cron & multi-reminders
- **SMTP** for email reminders (console in dev)
- **Django REST + Token auth** for login/signup and scheduling API
- **Minimal black web UI** for creating meetings

### Core backend pieces

- **`backend/schemas.py`**: `ScheduleRequest` – one Pydantic schema with:
  - Online / Offline mode (`MeetingMode` enum)
  - Application (`MeetingApp` enum: Meet / Zoom / Teams) + optional link
  - Optional location for onsite meetings
  - All times stored as native Python `datetime` in UTC
  - User timezone string (IANA) for display in emails
  - Multi-reminder config: `reminder_minutes_before`, `reminder_count`, `reminder_interval_minutes`
  - Optional cron expression (`cron_expression`) for recurring reminders
  - `json_created_at` auto timestamp (UTC)
- **`backend/llm_client.py`**:
  - Gemini integration (via `google-genai`) with JSON-only response
  - Fallback mode that treats `natural_text` as raw JSON for local testing
- **`backend/scheduler.py`**:
  - APScheduler setup (`BackgroundScheduler`)
  - Date triggers for multi-reminders and optional cron triggers
  - Timezone conversion via `zoneinfo`
  - Designated email format and SMTP send function
- **`backend/service.py`**:
  - End-to-end function `handle_natural_language_request()` that:
    - Accepts natural language
    - Calls Gemini
    - Validates into the single Pydantic schema
    - Schedules APScheduler jobs
    - Returns the validated object back to the web layer
- **`autosched_backend` (Django project)**:
  - REST + Token auth
  - Settings wired for `scheduler_core` app and console email backend
- **`scheduler_core` app**:
  - Starts a singleton APScheduler in `apps.py`
  - `views_auth.py` for signup/login
  - `views.py` for the `/api/schedule/` endpoint
- **`frontend/index.html`**:
  - Minimal black UI with:
    - Login / signup panel (Token auth)
    - Calendar-like meeting form (date, time, timezone, mode, platform, link, location)
    - Reminder configuration (how long before, how many times, interval)
    - Calls `/api/schedule/` with JSON payload

### How to run (development)

#### Step 1: Install Python dependencies

```bash
pip install Django djangorestframework pydantic apscheduler google-genai
```

#### Step 2: Run Django migrations

```bash
python manage.py migrate
```

#### Step 3: Start the Django backend server

```bash
python manage.py runserver
```

**Backend will be running at:** `http://127.0.0.1:8000`

**API Endpoints:**
- `POST http://127.0.0.1:8000/api/signup/` - Create account
- `POST http://127.0.0.1:8000/api/login/` - Login (returns token)
- `POST http://127.0.0.1:8000/api/schedule/` - Schedule meeting (requires token)

#### Step 4: Open the frontend

**Option A: Direct file open (simplest)**
- Navigate to the `frontend` folder
- Double-click `index.html` to open it in your browser

**Option B: Serve via Python HTTP server (recommended for CORS)**
```bash
cd frontend
python -m http.server 8080
```
Then open: `http://127.0.0.1:8080` in your browser

**Frontend URL:** `http://127.0.0.1:8080` (if using Python server) or `file:///path/to/frontend/index.html` (if opening directly)

#### Step 5: Use the application

1. **Sign up:** Create an account with username, email, and password
2. **Login:** Use your credentials to get an authentication token
3. **Schedule a meeting:** Fill in the form:
   - Date and time
   - Timezone (default: Asia/Kolkata)
   - Mode (online/offline)
   - Platform (Meet/Zoom/Teams) if online
   - Meeting URL or location
   - Reminder settings (minutes before, count, interval)
4. **Check reminders:** Reminder emails will appear in the Django server console (where you ran `runserver`)

#### Notes

- **Email backend:** Currently set to console output (emails print to terminal)
- **To enable real SMTP:** Update `EMAIL_BACKEND` and SMTP settings in `autosched_backend/settings.py`
- **Gemini API:** Set `GEMINI_API_KEY` environment variable if using real Gemini integration (otherwise falls back to JSON parsing)

