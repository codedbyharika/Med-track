from app.models import User, db

def test_register(client, app):
    response = client.post('/register', data={
        'email': 'new@example.com',
        'password': 'password123',
        'name': 'New User'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(email='new@example.com').first()
        assert user is not None
        assert user.name == 'New User'

def test_login_logout(client, app):
    # Setup user
    from app import bcrypt
    with app.app_context():
        hashed = bcrypt.generate_password_hash('pass').decode('utf-8')
        user = User(email='login@example.com', password_hash=hashed, name='Login User')
        db.session.add(user)
        db.session.commit()

    # Login
    response = client.post('/login', data={'email': 'login@example.com', 'password': 'pass'}, follow_redirects=True)
    assert b"Dashboard" in response.data
    
    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data
