# MediTrack

MediTrack is a web-based healthcare assistance platform designed for patients to manage their medications, appointments, and receive automated reminders. It features a simple rule-based chatbot for wellness support.

## Features

- **Medicine Management**: Track prescriptions, doses, and schedules.
- **Adherence Tracking**: Visual adherence percentage calculation.
- **Reminders**: Automated email reminders for missed doses (using Scheduler).
- **Appointments**: Book and manage medical appointments with conflict detection.
- **Chatbot**: Built-in assistant for quick help and mood tracking support.
- **Secure Auth**: Bcrypt password hashing and Flask-Login session management.

## Prerequisites

- Python 3.11+
- Docker (optional)

## Quick Start (Local)

1. **Setup Environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Configuration**
   Copy `.env.example` to `.env` and update SMTP settings if you want actual emails.
   ```bash
   cp .env.example .env
   ```

3. **Run Application**
   ```bash
   # Initialize DB and run
   flask run --debug
   ```
   Open [http://localhost:5000](http://localhost:5000)

4. **Seed Demo Data**
   ```bash
   python scripts/seed_demo.py
   ```
   Login with: `demo@meditrack.test` / `DemoPassword123`

## Running with Docker

```bash
docker-compose up --build
```
The app will be available at [http://localhost:5000](http://localhost:5000).

## Tests

Run the full test suite with coverage:
```bash
pytest --cov=app tests/
```

## Scheduler & API
- The background scheduler runs every minute to check for queued reminders.
- **API Endpoints**:
  - `POST /api/medicines`
  - `POST /api/medicines/<id>/log`
  - `POST /api/chat`
  - `POST /api/reminders/schedule` (Internal)
