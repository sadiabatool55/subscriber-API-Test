# Use official Python base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy everything into container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
