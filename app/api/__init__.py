"""
API package for handling REST endpoints.
"""
from flask import Blueprint

api = Blueprint('api', __name__)

# Import routes after creating blueprint to avoid circular imports
from . import routes