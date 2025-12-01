# Base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]
