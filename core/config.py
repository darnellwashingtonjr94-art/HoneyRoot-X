import os

class Config:
    # Server Settings
    BIND_PORT = int(os.environ.get("HONEYPORT", 2222))
    BIND_HOST = "0.0.0.0"
    HOST_KEY = "/opt/honeyroot/host_rsa_key"
    
    # Tar-pit Settings
    TARPIT_MIN = 3.0
    TARPIT_MAX = 7.0
    
    # Paths
    LOG_DIR = "/opt/honeyroot/logs"
    PAYLOAD_DIR = os.path.join(LOG_DIR, "payloads")
    LOG_FILE = os.path.join(LOG_DIR, "honeypot.json")
    
    # APIs
    VT_API_KEY = os.environ.get("VT_API_KEY", "")
