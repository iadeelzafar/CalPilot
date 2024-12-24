from flask import jsonify, request, current_app
from . import api
from typing import Dict, Any

def error_response(message: str, status_code: int = 400) -> tuple[Dict[str, Any], int]:
    """Create a standardized error response."""
    current_app.logger.error(f"API Error ({status_code}): {message}")
    return jsonify({'error': message}), status_code

@api.route('/call/<call_id>')
def get_call(call_id):
    """Get a specific call by ID."""
    if not call_id:
        return error_response("Call ID is required", 400)

    try:
        call = current_app.call_service.get_call_by_id(call_id)
        if call:
            return jsonify(call)
        return error_response("Call not found", 404)
    except Exception as e:
        return error_response(f"Failed to retrieve call: {str(e)}", 500)

@api.route('/calls/search')
def search_calls():
    """Search calls with optional filters."""
    try:
        query = request.args.get('query', '')
        company = request.args.get('company', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        calls = current_app.call_service.search_calls(
            query=query,
            company=company,
            date_from=date_from,
            date_to=date_to
        )
        return jsonify(calls)
    except ValueError as e:
        return error_response(f"Invalid search parameters: {str(e)}", 400)
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)

@api.route('/call/<call_id>/summary')
def get_call_summary(call_id):
    """Get summary information for a specific call."""
    if not call_id:
        return error_response("Call ID is required", 400)

    try:
        summary = current_app.call_service.get_call_summary(call_id)
        if summary:
            return jsonify(summary)
        return error_response("Call not found", 404)
    except Exception as e:
        return error_response(f"Failed to generate summary: {str(e)}", 500)

@api.route('/ask', methods=['POST'])
def ask_question():
    """Ask a question about a specific call using AI."""
    try:
        data = request.get_json()
        if not data:
            return error_response("No JSON data provided", 400)

        call_id = data.get('call_id')
        question = data.get('question')

        if not call_id:
            return error_response("call_id is required", 400)
        if not question:
            return error_response("question is required", 400)

        call = current_app.call_service.get_call_by_id(call_id)
        if not call:
            return error_response("Call not found", 404)

        answer = current_app.claude_service.get_response(
            call_id=call_id,
            question=question,
            transcript=call['transcript']['text']
        )
        return jsonify({'answer': answer})

    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Failed to process question: {str(e)}", 500)

@api.route('/calls/refresh', methods=['POST'])
def refresh_calls():
    """Force refresh the calls cache."""
    try:
        current_app.call_service.refresh_cache()
        # Clear the get_unique_companies cache
        current_app.call_service.get_unique_companies.cache_clear()
        return jsonify({'message': 'Cache refreshed successfully'})
    except Exception as e:
        return error_response(f"Failed to refresh cache: {str(e)}", 500) 