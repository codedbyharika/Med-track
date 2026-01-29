import sys
import os

# Add parent dir to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db, bcrypt
from app.models import User, Medicine, Appointment, DoseLog
from datetime import datetime, timedelta

def seed():
    app = create_app()
    with app.app_context():
        # Clear existing
        db.drop_all()
        db.create_all()
        
        # User
        password = 'DemoPassword123'
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email='demo@meditrack.test', password_hash=hashed, name='Demo Patient')
        db.session.add(user)
        db.session.commit()
        
        print(f"Created user: demo@meditrack.test / {password}")
        
        # Medicine
        med1 = Medicine(
            user_id=user.id,
            name="Atorvastatin",
            dose="10mg",
            times='["09:00", "21:00"]',
            start_date=datetime.now() - timedelta(days=2),
            end_date=datetime.now() + timedelta(days=30)
        )
        med2 = Medicine(
            user_id=user.id,
            name="Lisinopril",
            dose="5mg",
            times='["08:00"]',
            start_date=datetime.now() - timedelta(days=5)
        )
        db.session.add_all([med1, med2])
        db.session.commit()
        
        # Appointment
        appt = Appointment(
            user_id=user.id,
            title="Cardiology Follow-up",
            description="Routine checkup",
            appointment_datetime=datetime.now() + timedelta(days=2, hours=3)
        )
        db.session.add(appt)
        db.session.commit()
        
        print("Seeded Medicines and Appointments.")

if __name__ == '__main__':
    seed()
