import os
import json
from core.logger import log_event, LOG_FILE

def test_log_event_writes_valid_json():
    # Ensure starting clean
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        
    test_data = {"ip": "192.168.1.1", "user": "admin"}
    log_event("test_event", test_data)
    
    assert os.path.exists(LOG_FILE)
    
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        
        event = json.loads(lines[0])
        assert event["event_type"] == "test_event"
        assert event["payload"]["ip"] == "192.168.1.1"
        assert "timestamp" in event
