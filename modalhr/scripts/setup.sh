#!/bin/bash

# Initialize project
echo "🚀 Initializing HRMIS project..."

# Create virtual environment
echo "🛠 Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -U pip setuptools wheel
pip install -r requirements/development.txt

# Set environment variables
echo "🔧 Setting environment variables..."
export SECRET_KEY="your-secret-key-here"
export DEBUG="True"
export REDIS_URL="redis://localhost:6379/0"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# Run migrations
echo "🗄 Running migrations..."
python manage.py migrate

# Create superuser
echo "👑 Creating superuser..."
python manage.py createsuperuser

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start services
echo "✅ Setup complete!"
echo "👉 Start the development server with: python manage.py runserver"
echo "👉 Start Celery worker with: celery -A config worker -l info"
echo "👉 Start Celery beat with: celery -A config beat -l info"