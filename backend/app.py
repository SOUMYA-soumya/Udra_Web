from flask import Flask
from flask_cors import CORS
from models import db
from auth import auth_bp
from user_admin import admin_bp  # 1. Import the new blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///udrachallan.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # 2. Register the blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp) 

    with app.app_context():
        db.create_all() 

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
