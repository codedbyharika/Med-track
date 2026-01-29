# Demo Instructions

Follow these steps to verify the application functionality.

## 1. Setup
Ensure you have run the seed script:
```bash
python scripts/seed_demo.py
```

## 2. Walkthrough Steps

1. **Login**
   - Go to `http://localhost:5000/login`
   - User: `demo@meditrack.test`
   - Pass: `DemoPassword123`

2. **Dashboard**
   - Verify you see "Atorvastatin" and "Lisinopril" in the adherence chart.
   - Verify adherence values (initially 0% or based on logs if you added any).

3. **Medicine Management**
   - Click "Manage Medicines".
   - Click "Add Medicine".
   - Enter: "Vitamin D", "1000IU", "08:00", Start Today.
   - Click "Save".
   - Verify it appears in the list.

4. **Log Dose**
   - On the Medicines page, click "Log Taken" for "Vitamin D".
   - Verify success alert and page reload. Adherence should update to 100% (1/1).

5. **Appointments**
   - Go to Appointments (via Dashboard "Appointments" button or URL if implemented UI link).
   - *Note: If UI link missing, use /appointments directly*.
   - Verify "Cardiology Follow-up" exists.
   - Click "Book Appointment".
   - Try to book same time as existing (conflict check).
   - Book a valid time.

6. **Chatbot**
   - Go to Chatbot (`/chat`).
   - Type "I feel anxious".
   - Verify response offers support.
   - Type "I have an appointment".
   - Verify response mentions appointments section.

## 3. Email Reminders (SMTP Debug)
To test emails without real SMTP:
1. Run local debug server: `python -m smtpd -n -c DebuggingServer localhost:1025`
2. Update `.env`: `SMTP_HOST=localhost`, `SMTP_PORT=1025`
3. Restart Flask.
4. Wait 1 minute. You should see reminder emails printed in the debug console for "Atorvastatin" etc if timed correctly (or just add a new med scheduled for *now*).
