import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    CALLS_FILE = os.environ.get('CALLS_FILE', 'data/calls.json')
    GCS_BUCKET = os.environ.get('GCS_BUCKET')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    CALLS_FILE = 'test_calls.json'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Map config names to config objects
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}