# Use Python base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY kisanmitra-31972-firebase-adminsdk-fbsvc-44ae0d4b73.json /app/credentials/firebase.json
COPY .env /app/.env

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Use gunicorn to run the app
CMD ["gunicorn", "kisanmitra_backend.wsgi:application", "--bind", "0.0.0.0:8080"]
