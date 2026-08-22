FROM python:3.11-slim

# Install necessary crypto dependencies for Paramiko
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for the container process
RUN useradd -m -s /bin/bash honeyuser

WORKDIR /opt/honeyroot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ core/
COPY docker/entrypoint.sh .

# Generate a persistent host key
RUN ssh-keygen -t rsa -f /opt/honeyroot/host_rsa_key -N ''

RUN mkdir -p logs && \
    chown -R honeyuser:honeyuser /opt/honeyroot && \
    chmod +x entrypoint.sh

USER honeyuser

# Expose the fake SSH port
EXPOSE 2222

ENTRYPOINT ["./entrypoint.sh"]
