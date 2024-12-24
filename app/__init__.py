"""
CalPilot: AI-powered call analysis platform
Developed by Adeel Zafar (www.adeelzafar.com)
"""

from flask import Flask
from app.config import config
from app.services import CallService, ClaudeService
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_name="development"):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load config
    if isinstance(config_name, str):
        app.config.from_object(config[config_name])
    else:
        app.config.from_object(config_name)
    
    # Configure logging
    if not app.debug:
        # Ensure logs directory exists
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Set up rotating file handler
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=1024 * 1024,  # 1MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('CalPilot startup')
    
    # Initialize services
    app.call_service = CallService(app)
    app.claude_service = ClaudeService(app)
    
    # Register blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Register API routes
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app
