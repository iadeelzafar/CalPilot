# CalPilot

![image](https://github.com/user-attachments/assets/ee8a6915-cc9a-4878-8ed3-a3e1d29a0540)

An AI-powered call analysis platform for reviewing and analyzing sales calls.

Developed by [Adeel Zafar](https://www.adeelzafar.com)

## Local Development Setup

1. Copy example environment file and configure your keys:
```bash
cp .env.example .env
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up local environment:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env.local with your settings
nano .env

# Create development data directory
mkdir -p data
cp your_calls.json data/calls.json
```

5. Run the application:
```bash
flask run
```

## Project Structure
- `app/`: Main application package
  - `api/`: API endpoints
  - `services/`: Business logic
  - `templates/`: HTML templates
  - `static/`: Static files
- `data/`: Local development data
- `config.py`: Configuration settings
- `tests/`: Test suite

## Development
- Built with Flask and Anthropic's Claude API <3
- Frontend using Tailwind CSS
- Comprehensive test suite
- Caching for performance
- Environment-specific configurations

### Core Technologies
- **Flask**: Lightweight web framework with excellent extensibility
- **Anthropic Claude API**: State-of-the-art AI for natural language processing
- **Google Cloud Platform**: Scalable cloud infrastructure
  - Cloud Run for containerized deployment
  - Cloud Storage for secure data management

### Key Libraries
- `anthropic`: Official Claude AI SDK for intelligent call analysis
- `python-dotenv`: Secure environment configuration management
- `gunicorn`: Production-grade WSGI server
- `pytest`: Comprehensive testing framework

### Advanced Features
- **Intelligent Caching**:
  - LRU cache for optimized duration formatting
  - Time-based cache invalidation for call data
  - Environment-specific cache strategies

- **Robust Logging**:
  - Rotating file handlers with 1MB limit
  - Structured logging with line numbers
  - Environment-aware log levels
  - Comprehensive error tracking

- **Error Handling**:
  - Graceful API error management
  - Rate limiting protection
  - Timeout handling
  - Detailed error reporting

- **Security**:
  - Environment-based configurations
  - Secure credential management
  - Cloud-native security practices

## Features

### Recent Calls
![image](https://github.com/user-attachments/assets/3caefef3-1de1-4cd1-aea7-b017ea459ce6)

### Filter calls by date
![image](https://github.com/user-attachments/assets/ffd01d8a-3fd9-44f9-ad1f-22446b5e95d3)

### Search for calls
![image](https://github.com/user-attachments/assets/680baa10-6ae3-496b-8cc9-660ebc1a996e)

### List of companies
![image](https://github.com/user-attachments/assets/45a0a158-67ca-4e80-9d6f-edf24f7e745c)

### Call summary and Key topics
![image](https://github.com/user-attachments/assets/9675731d-2878-4cec-b23c-1de592a4071d)

### Pre-determined questions for each call
![image](https://github.com/user-attachments/assets/c7634b15-7d76-480a-b6f7-cbf7ae66da7e)

### Asking your own questions
![image](https://github.com/user-attachments/assets/f7b8ca45-6dde-402d-8360-fdf57a2fbf42)

### Answer from Claude <3
![image](https://github.com/user-attachments/assets/038a384a-88b4-4bcd-884d-e90b08405f99)

## License
MIT License
