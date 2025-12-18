# Quick Start Guide - AutoSched-AI

## 🚀 Running the Application

### Backend (Django REST API)

**Current Status:** ✅ Server is running at `http://127.0.0.1:8000`

**To start the backend:**

```bash
# Navigate to project directory
cd "C:\Users\Lenovo\OneDrive\git kanak\AutoSched-AI"

# Install dependencies (if not already installed)
pip install Django djangorestframework pydantic apscheduler google-genai

# Run migrations (first time only)
python manage.py migrate

# Start the server
python manage.py runserver
```

**Backend URLs:**
- API Base: `http://127.0.0.1:8000`
- Signup: `http://127.0.0.1:8000/api/signup/`
- Login: `http://127.0.0.1:8000/api/login/`
- Schedule: `http://127.0.0.1:8000/api/schedule/`

### Frontend (Web UI)

**Option 1: Open directly in browser**
- Navigate to: `frontend\index.html`
- Double-click the file to open in your default browser
- URL will be: `file:///C:/Users/Lenovo/OneDrive/git kanak/AutoSched-AI/frontend/index.html`

**Option 2: Serve via Python HTTP server (recommended)**
```bash
cd frontend
python -m http.server 8080
```
- Then open: `http://127.0.0.1:8080` in your browser

## 📋 Quick Commands Summary

```bash
# 1. Install dependencies
pip install Django djangorestframework pydantic apscheduler google-genai

# 2. Setup database (first time)
python manage.py migrate

# 3. Start backend server
python manage.py runserver

# 4. (In a new terminal) Start frontend server (optional)
cd frontend
python -m http.server 8080
```

## 🔗 Access Links

- **Backend API:** http://127.0.0.1:8000
- **Frontend UI:** http://127.0.0.1:8080 (if using Python server) or open `frontend/index.html` directly

## 📝 Usage

1. Open the frontend in your browser
2. **Sign up** with username, email, password
3. **Login** to get your authentication token
4. **Schedule a meeting:**
   - Fill in date, time, timezone
   - Select mode (online/offline)
   - Add platform (Meet/Zoom/Teams) and URL if online
   - Set reminder preferences
   - Click "Schedule meeting"
5. **Check reminders:** They will appear in the Django server console

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where `runserver` is running.

