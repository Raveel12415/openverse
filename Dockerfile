# Use the Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional, for production)
RUN python manage.py collectstatic --noinput

# Expose port (Django default)
EXPOSE 8000

# Start the Django app
CMD ["gunicorn", "applications.wsgi:application", "--bind", "0.0.0.0:8000"]
