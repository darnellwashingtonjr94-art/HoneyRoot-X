import json
import logging
import os
from datetime import datetime, timezone

LOG_DIR = "/opt/honeyroot/logs"
LOG_FILE = os.path.join(LOG_DIR, "honeypot.json")

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Standard Python logger fallback
logging.basicConfig(level=logging.INFO, format='%(message)s')

def log_event(event_type: str, data: dict):
    """
    Logs events in a structured JSON format for SIEM ingestion.
    """
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "payload": data
    }
    
    log_line = json.dumps(event)
    logging.info(log_line)
    
    # Append to JSON log file
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_line + "\n")
    except IOError as e:
        logging.error(f"Failed to write to log file: {e}")
