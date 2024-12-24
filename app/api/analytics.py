from flask import jsonify, current_app
from . import api

@api.route('/analytics/companies')
def get_companies():
    """Get list of all unique companies."""
    companies = current_app.call_service.get_unique_companies()
    return jsonify(companies) 