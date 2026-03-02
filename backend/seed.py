from app import create_app
from models import db, User, Role
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

def seed_database():
    app = create_app()
    with app.app_context():
        print("🌱 Starting database seed process...")

        # 1. Clear existing data (useful for development)
        db.drop_all()
        db.create_all()
        print("🧹 Database wiped and tables recreated.")

        # 2. Define the Core RBAC Modules and Roles
        roles_data = [
            Role(role_name='Super Admin', module_name='Security Admin', can_create=True, can_read=True, can_update=True, can_delete=True),
            Role(role_name='Data Entry', module_name='Challan Entry', can_create=True, can_read=True, can_update=False, can_delete=False),
            Role(role_name='Finance Manager', module_name='Financial Redemption', can_create=False, can_read=True, can_update=True, can_delete=False),
            Role(role_name='Logistics Viewer', module_name='Transporter Directory', can_create=False, can_read=True, can_update=False, can_delete=False)
        ]
        
        db.session.add_all(roles_data)
        db.session.commit() # Commit roles first so we can assign them
        print("🔐 RBAC Roles and Modules seeded.")

        # 3. Create the First Super Admin User
        # We use generate_password_hash to ensure even the DB admin can't read the password
        super_admin = User(
            username='som_admin',
            full_name='System Administrator',
            phone_number='+910000000000',
            govt_id_type='PAN',
            govt_id_number='ABCDE1234F',
            status='Active', # Must be active to pass our login middleware!
            password_hash=generate_password_hash('UdraSecure2026!')
        )

        # 4. Assign the Super Admin role to this user
        admin_role = Role.query.filter_by(role_name='Super Admin').first()
        super_admin.roles = [admin_role] # Assuming you added a relationship in models.py

        db.session.add(super_admin)
        db.session.commit()
        print("🧑‍💻 Initial Super Admin 'som_admin' created successfully.")
        
        print("✅ Seeding complete! You can now log into the Udra Challan Portal.")

if __name__ == '__main__':
    seed_database()
