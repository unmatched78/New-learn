# backend/Dockerfile

# 1. Use a lightweight Python base
FROM python:3.11-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create and set working directory
WORKDIR /app

# 4. Install system dependencies (if any)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the entire Django project into /app
COPY . /app/

# 7. Collect static files (if you have any)
#    RUN python manage.py collectstatic --noinput

# 8. Expose port 8000
EXPOSE 8000

# 9. Default command: run Django development server
CMD ["gunicorn", "djtest.wsgi:application", "--bind", "0.0.0.0:8000"]
