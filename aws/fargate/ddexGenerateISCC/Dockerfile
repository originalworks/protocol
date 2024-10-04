# Start with an official Python image
# Uses Debain bookworm by default
FROM python:3.8

# Set environment variables
ENV HOME=/tmp
ENV ISCC_EXIV2_BIN=/usr/bin/exiv2

# Install dependencies
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    libmagic1 \
    && apt-get clean

# Download and manually install the expected version of exiv2

RUN mkdir -p /tmp/.local/share/iscc-sdk/ && \
    curl -Lo /tmp/.local/share/iscc-sdk/exiv2-0.27.2-Linux64.tar.gz \
    https://github.com/Exiv2/exiv2/releases/download/v0.27.2/exiv2-0.27.2-Linux64.tar.gz && \
    tar -xzvf /tmp/.local/share/iscc-sdk/exiv2-0.27.2-Linux64.tar.gz -C /tmp/.local/share/iscc-sdk/ && \
    mv /tmp/.local/share/iscc-sdk/exiv2-0.27.2-Linux64/bin/exiv2 /tmp/.local/share/iscc-sdk/exiv2 && \
    chmod +x /tmp/.local/share/iscc-sdk/exiv2

# Add the directory to PATH
ENV PATH="/tmp/.local/share/iscc-sdk:$PATH"

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Run the Python script (change to your function's entry point)
CMD ["python", "main.py"]