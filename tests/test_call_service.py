import pytest
from datetime import datetime

def test_load_calls(app):
    """Test loading calls from file."""
    with app.app_context():
        calls = app.call_service.load_calls()
        assert len(calls) == 1
        assert calls[0]['call_metadata']['duration'] == 900
        assert app.call_service.format_duration(900) == '15m'

def test_get_call_by_id(app):
    """Test retrieving a specific call by ID."""
    with app.app_context():
        call = app.call_service.get_call_by_id('test-call-1')
        assert call is not None
        assert call['call_metadata']['title'] == 'Test Sales Call 1'

def test_search_calls(app):
    """Test search functionality."""
    with app.app_context():
        # Search by text
        results = app.call_service.search_calls(query='pricing')
        assert len(results) == 1

def test_get_call_summary(app):
    """Test getting call summary."""
    with app.app_context():
        summary = app.call_service.get_call_summary('test-call-1')
        assert summary is not None
        assert summary['summary'] == 'Test call summary'

def test_get_unique_companies(app):
    """Test getting unique companies."""
    with app.app_context():
        companies = app.call_service.get_unique_companies()
        assert len(companies) == 2
        assert 'company1' in companies
        assert 'prospect' in companies

def test_format_duration(app):
    """Test duration formatting."""
    with app.app_context():
        assert app.call_service.format_duration(3600) == '1h'
        assert app.call_service.format_duration(3660) == '1h 1m'
        assert app.call_service.format_duration(60) == '1m'
        assert app.call_service.format_duration(90) == '1m 30s' 