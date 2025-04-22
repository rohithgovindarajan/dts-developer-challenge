# src/main/python/uk/gov/hmcts/reform/dev/Application.py

import os, sys
from pathlib import Path
from flask import Flask
from flask_basicauth import BasicAuth
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from the .env file located at the repository root
repo_root = Path(__file__).parents[8]
load_dotenv(dotenv_path=repo_root / '.env')

# Add the src/main/python directory to the Python module search path
sys.path.insert(0, str(repo_root / 'src' / 'main' / 'python'))

# Shared extensions for the Flask app
db = SQLAlchemy()  # SQLAlchemy for database interactions
migrate = Migrate()  # Flask-Migrate for database migrations
basic_auth = BasicAuth()  # Basic authentication for securing endpoints

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(
        __name__,
        static_folder=str(repo_root / 'src' / 'main' / 'resources' / 'static'),  # Static files directory
        static_url_path=''  # URL path for serving static files
    )
    
    # Update app configuration with environment variables and database settings
    app.config.update({
        'BASIC_AUTH_USERNAME': os.getenv('BASIC_AUTH_USERNAME'),  # Basic Auth username
        'BASIC_AUTH_PASSWORD': os.getenv('BASIC_AUTH_PASSWORD'),  # Basic Auth password
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + str(repo_root / 'tasks.db'),  # SQLite database URI
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,  # Disable SQLAlchemy event notifications
    })

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)
    
    # Initialize shared extensions with the app
    basic_auth.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Automatically create database tables in development mode
    with app.app_context():
        db.create_all()

    # Register routes and error handlers
    from uk.gov.hmcts.reform.dev.controllers import tasks_bp  # Import task-related routes
    from uk.gov.hmcts.reform.dev.errors import register_error_handlers  # Import error handlers

    app.register_blueprint(tasks_bp)  # Register the tasks blueprint
    register_error_handlers(app)  # Register custom error handlers

    @app.route('/')
    def root():
        """
        Serve the index.html file as the root endpoint.
        """
        return app.send_static_file('index.html')

    return app

# Module-level app instance for CLI commands and migrations
app = create_app()
app.debug = True  # Enable debug mode for development
