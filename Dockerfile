# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements-web.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-web.txt

# Copy application files
COPY web_app_production.py .
COPY templates/ ./templates/
COPY bestmodel.h5 .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=web_app_production.py
ENV FLASK_ENV=production
ENV PORT=5000

# Run the application
CMD ["python", "web_app_production.py"]

