from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from models import db, User, LoginAudit

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 1. Extract request data
    username = data.get('username')
    password = data.get('password') # In a real app, compare this against password_hash
    ip_address = request.remote_addr or 'Unknown'

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    # 2. Query the user
    user = User.query.filter_by(username=username).first()

    # 3. Determine Login Status
    login_status = 'Failed'
    response_data = {}
    http_code = 401

    if user:
        if user.status != 'Active':
            response_data = {'error': 'Account is Inactive. Please contact the Security Admin.'}
            http_code = 403
        else:
            # Placeholder: Here you would use werkzeug.security.check_password_hash
            # Assuming password is correct for this workflow demonstration:
            login_status = 'Success'
            response_data = {
                'message': 'Login successful',
                'user': {
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': 'Assigned Roles Placeholder'
                },
                'token': 'secure_jwt_token_placeholder' # This token is sent to the Flutter frontend
            }
            http_code = 200
    else:
        response_data = {'error': 'Invalid credentials'}

    # 4. Enforce Mandatory Audit Trail
    audit_entry = LoginAudit(
        username=username if username else 'Unknown',
        login_datetime=datetime.now(timezone.utc),
        ip_address=ip_address,
        status=login_status
    )
    
    db.session.add(audit_entry)
    db.session.commit()

    # 5. Return response to Flutter frontend
    return jsonify(response_data), http_code
