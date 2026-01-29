import json
from datetime import datetime, timedelta
from app.models import Medicine, DoseLog, db
from app.utils import calculate_adherence

def test_add_medicine(auth_client, app):
    data = {
        'name': 'Test Med',
        'dose': '10mg',
        'times': ['09:00'],
        'start_date': datetime.now().strftime('%Y-%m-%d')
    }
    response = auth_client.post('/api/medicines', json=data)
    assert response.status_code == 201
    
    with app.app_context():
        med = Medicine.query.filter_by(name='Test Med').first()
        assert med is not None
        assert med.dose == '10mg'

def test_adherence_perfect(auth_client, app):
    # 1. Create Medicine (Start 5 days ago, 1 time per day = 5 scheduled)
    start_date = datetime.now() - timedelta(days=5)
    end_date = datetime.now()
    
    with app.app_context():
        from flask_login import current_user
        # Need to get user id from email since auth_client session is active but context is new
        # Easier to just rely on auth_client logic or query user
        from app.models import User
        user = User.query.filter_by(email='test@example.com').first()
        
        med = Medicine(
            user_id=user.id,
            name="Perfect Med",
            dose="1 pill",
            times='["08:00"]',
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(med)
        db.session.commit()
        med_id = med.id
        
        # 2. Log 6 doses (today inclusive makes 6 days: -5, -4, -3, -2, -1, 0)
        # Actually loop 0 to 5
        for i in range(6):
            log = DoseLog(medicine_id=med_id, scheduled_datetime=datetime.now(), taken=True)
            db.session.add(log)
        db.session.commit()
        
        # 3. Calculate
        # Scheduled: -5 to now (approx 6 occurrences depending on time). 
        # For robustness let's just trust utils logic.
        adh = calculate_adherence(med_id)
        assert adh == 100.0

def test_dose_log_endpoint(auth_client, app):
    # Add med first
    auth_client.post('/api/medicines', json={
        'name': 'Log Med', 'dose': '5mg', 'times': ['10:00'], 'start_date': '2025-01-01'
    })
    
    with app.app_context():
        med = Medicine.query.filter_by(name='Log Med').first()
        med_id = med.id
        
    response = auth_client.post(f'/api/medicines/{med_id}/log', json={
        'scheduled_datetime': '2025-01-01T10:00:00',
        'taken': True
    })
    assert response.status_code == 200
    assert 'adherence' in response.json
