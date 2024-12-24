from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
def splash():
    """Landing page with animated logo."""
    return render_template('splash.html')

@main.route('/dashboard')
def dashboard():
    """Main dashboard showing call list and search interface."""
    calls = current_app.call_service.load_calls()
    companies = current_app.call_service.get_unique_companies()
    return render_template('index.html', calls=calls, companies=companies)
