from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .models import db, User

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the default configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    migrate = Migrate(app, db)
    
    # Register blueprints
    from .routes import main, auth, admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    return app
