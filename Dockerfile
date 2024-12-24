# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Cloud Run will set PORT environment variable
ENV PORT 8080
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 "app:create_app('production')" 