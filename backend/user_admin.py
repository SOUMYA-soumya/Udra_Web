from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, User, Role

# Create a Blueprint for the Security Admin routes
admin_bp = Blueprint('admin', __name__)

# Helper function to simulate RBAC Middleware
def check_admin_permission(admin_username):
    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user or admin_user.status != 'Active':
        return None, False
    
    # Check if this user has the 'Super Admin' role or 'User Admin' permissions
    has_permission = any(role.role_name == 'Super Admin' or role.module_name == 'Security Admin' for role in admin_user.roles)
    return admin_user, has_permission

@admin_bp.route('/api/admin/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # 1. Identify who is making the request (In a real app, extract this from a secure JWT token header)
    requester_username = data.get('admin_username') 
    admin_user, has_permission = check_admin_permission(requester_username)
    
    if not has_permission:
        return jsonify({'error': 'RBAC Access Denied: You do not have permission to provision users.'}), 403

    # 2. Extract new user mandatory data
    new_username = data.get('username')
    full_name = data.get('full_name')
    phone = data.get('phone_number')
    govt_id_type = data.get('govt_id_type') # e.g., PAN, Aadhaar
    govt_id_number = data.get('govt_id_number')
    raw_password = data.get('password')
    assigned_role_names = data.get('roles', []) # List of role names like ['Data Entry', 'Logistics Viewer']

    # Basic validation
    if not all([new_username, full_name, phone, govt_id_type, govt_id_number, raw_password]):
        return jsonify({'error': 'Missing mandatory user data fields'}), 400

    if User.query.filter_by(username=new_username).first():
        return jsonify({'error': 'Username already exists'}), 409

    # 3. Create the new user and ENFORCE THE AUDIT TRAIL
    new_user = User(
        username=new_username,
        full_name=full_name,
        phone_number=phone,
        govt_id_type=govt_id_type,
        govt_id_number=govt_id_number,
        status='Inactive', # Users must be explicitly activated later!
        password_hash=generate_password_hash(raw_password),
        created_by=admin_user.id # MANDATORY AUDIT: Tracking who created this account
    )

    # 4. Map the Granular Roles
    if assigned_role_names:
        roles_to_assign = Role.query.filter(Role.role_name.in_(assigned_role_names)).all()
        new_user.roles = roles_to_assign

    # 5. Save to Database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': f'User {full_name} successfully provisioned.',
        'user_id': new_user.id,
        'status': new_user.status
    }), 201

@admin_bp.route('/api/admin/users', methods=['GET'])
def list_users():
    # Simple route to view the user directory
    requester_username = request.args.get('admin_username')
    _, has_permission = check_admin_permission(requester_username)
    
    if not has_permission:
        return jsonify({'error': 'RBAC Access Denied'}), 403

    users = User.query.all()
    user_list = []
    for u in users:
        user_list.append({
            'id': u.id,
            'username': u.username,
            'full_name': u.full_name,
            'status': u.status,
            'roles': [r.role_name for r in u.roles]
        })
        
    return jsonify({'users': user_list}), 200
