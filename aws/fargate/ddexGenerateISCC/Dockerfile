# Start with an official Python image from Docker Hub
FROM python:3.8-slim

# Set environment variables
ENV HOME=/tmp

# Install dependencies
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    libmagic1 \
    && apt-get clean

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Run the Python script (change to your function's entry point)
CMD ["python", "main.py"]

