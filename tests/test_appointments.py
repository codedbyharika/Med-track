from datetime import datetime, timedelta

def test_create_appointment(auth_client, app):
    # Future date
    dt = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
    
    response = auth_client.post('/api/appointments', json={
        'title': 'Checkup',
        'description': 'Regular',
        'datetime': dt
    })
    assert response.status_code == 201

def test_appointment_conflict(auth_client, app):
    now = datetime.now()
    # Create first appt
    dt1 = (now + timedelta(days=1)).replace(minute=0).strftime('%Y-%m-%dT%H:%M')
    auth_client.post('/api/appointments', json={'title': 'A', 'datetime': dt1})
    
    # Create overlapping appt (15 mins later)
    dt2 = (now + timedelta(days=1)).replace(minute=15).strftime('%Y-%m-%dT%H:%M')
    response = auth_client.post('/api/appointments', json={'title': 'B', 'datetime': dt2})
    
    assert response.status_code == 409
    assert b'Conflict' in response.data
