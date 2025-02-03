from app import app, db
from models import User

with app.app_context():
    admin_email = 'admin@example.com'
    admin_password = 'adminpassword'

    admin_user = User(email=admin_email, role='admin')
    admin_user.set_password(admin_password)
    db.session.add(admin_user)
    db.session.commit()
    print(f'Admin user {admin_email} created.')
