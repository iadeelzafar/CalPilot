# CalPilot

An AI-powered call analysis platform for reviewing and analyzing sales calls.

Developed by [Adeel Zafar](https://www.adeelzafar.com)

## Features
- View and search sales calls
- Filter calls by company and date
- Get AI-powered answers about call content
- View call summaries and key metrics
- Interactive interface with real-time updates

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

## Production Deployment (Google Cloud)
https://calpilot-311587764725.us-central1.run.app/
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
- Built with Flask and Anthropic's Claude API
- Frontend using Tailwind CSS
- Comprehensive test suite
- Caching for performance
- Environment-specific configurations

## License
MIT License
