from flask import jsonify, request, current_app
from . import api

@api.route('/call/<call_id>')
def get_call(call_id):
    """Get a specific call by ID."""
    call = current_app.call_service.get_call_by_id(call_id)
    if call is None:
        return jsonify({'error': 'Call not found'}), 404
    return jsonify(call)

@api.route('/calls/search')
def search_calls():
    """Search calls with optional filters."""
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

@api.route('/call/<call_id>/summary')
def get_call_summary(call_id):
    """Get summary for a specific call."""
    summary = current_app.call_service.get_call_summary(call_id)
    if summary is None:
        return jsonify({'error': 'Summary not found'}), 404
    return jsonify(summary)

@api.route('/companies')
def get_companies():
    """Get list of unique companies."""
    companies = current_app.call_service.get_unique_companies()
    return jsonify(companies)

@api.route('/ask', methods=['POST'])
def ask_question():
    """Ask a question about a call using Claude."""
    try:
        data = request.get_json()
        if not data or 'question' not in data or 'call_id' not in data:
            return jsonify({
                'error': 'Missing required fields: question and call_id'
            }), 400

        question = data['question']
        call_id = data['call_id']

        # Get the call first
        call = current_app.call_service.get_call_by_id(call_id)
        if not call:
            return jsonify({'error': 'Call not found'}), 404

        # Use Claude service to get answer
        answer = current_app.claude_service.ask_question(question, call)
        
        return jsonify({
            'answer': answer,
            'call_id': call_id,
            'question': question
        })

    except Exception as e:
        current_app.logger.error(f"Error processing question: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 