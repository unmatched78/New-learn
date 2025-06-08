# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements/development.txt

# Set environment variables
export SECRET_KEY="your-secret-key"
export DEBUG=True
export REDIS_URL="redis://localhost:6379/0"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start services in different terminals
python manage.py runserver
celery -A config worker -l info
celery -A config beat -l info