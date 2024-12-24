from app import create_app
from config import config

# Default to development configuration
app = create_app(config['development'])

if __name__ == '__main__':
    app.run(debug=True)
