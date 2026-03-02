from flask import Flask
from models import db
from auth import auth_bp  # Import the new blueprint

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///udrachallan.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Register the authentication routes
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all() 

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
