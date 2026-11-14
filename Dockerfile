# Start from an official image that already has Python
FROM python:3.13-slim

# The working folder inside the container
WORKDIR /app

# Install the packages first (Docker caches this step)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# The port the server listens on
EXPOSE 8000

# When the container starts: create the tables, then run the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]