import pytest
import json

def test_get_call(client):
    """Test getting a specific call."""
    response = client.get('/api/call/test-call-1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['call_metadata']['title'] == 'Test Sales Call 1'

def test_search_calls(client):
    """Test searching calls."""
    response = client.get('/api/calls/search?query=pricing')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1

def test_get_call_summary(client):
    """Test getting call summary."""
    response = client.get('/api/call/test-call-1/summary')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['summary'] == 'Test call summary'

def test_get_companies(client):
    """Test getting unique companies."""
    response = client.get('/api/companies')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert 'company1' in data
    assert 'prospect' in data 

def test_ask_question(client):
    """Test asking questions about calls."""
    # Test successful question
    response = client.post('/api/ask', json={
        'question': 'What was discussed?',
        'call_id': 'test-call-1'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data
    
    # Test missing data
    response = client.post('/api/ask', json={})
    assert response.status_code == 400
    
    # Test invalid call ID
    response = client.post('/api/ask', json={
        'question': 'What was discussed?',
        'call_id': 'invalid-id'
    })
    assert response.status_code == 404 