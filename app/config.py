import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    CALLS_FILE = "data/calls.json"
    GCS_BUCKET = None
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    TESTING = False
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    CALLS_FILE = "tests/data/test_calls.json"
    WTF_CSRF_ENABLED = False
    # Use memory storage for testing
    GCS_BUCKET = None
    # Test API key
    ANTHROPIC_API_KEY = 'test-key'

class ProductionConfig(Config):
    """Production configuration."""
    ENV = 'production'
    GCS_BUCKET = "calpilot-data"

# Map environment names to config objects
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
} 