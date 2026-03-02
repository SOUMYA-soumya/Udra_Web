from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

# 1. The Mandatory Audit Foundation
class BaseModel(db.Model):
    __abstract__ = True 

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    update_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

# 2. User Directory Model
class User(BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(120), unique=True, nullable=False) 
    full_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    
    govt_id_type = db.Column(db.String(50), nullable=False) 
    govt_id_number = db.Column(db.String(100), nullable=False, unique=True)
    
    status = db.Column(db.String(20), default='Inactive', nullable=False) 
    password_hash = db.Column(db.String(256), nullable=False)

    # Establish the Many-to-Many relationship with Roles
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

# 3. Dedicated Login Audit Table
class LoginAudit(db.Model):
    __tablename__ = 'login_audits'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    login_datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False) 

# 4. Role & Module Mapping (The RBAC Foundation)
class Role(BaseModel):
    __tablename__ = 'roles'
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    module_name = db.Column(db.String(100), nullable=False) 
    
    can_create = db.Column(db.Boolean, default=False)
    can_read = db.Column(db.Boolean, default=False)
    can_update = db.Column(db.Boolean, default=False)
    can_delete = db.Column(db.Boolean, default=False)

# Association table for User <-> Roles 
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)
