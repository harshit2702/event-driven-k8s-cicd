FROM python:3.9-slim

# Install kubectl
RUN apt-get update && \
    apt-get install -y curl && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

# Install Python dependencies
RUN pip install requests

# Copy the monitor script
COPY monitor.py /app/monitor.py
WORKDIR /app

# Run the monitor
CMD ["python", "monitor.py"]
