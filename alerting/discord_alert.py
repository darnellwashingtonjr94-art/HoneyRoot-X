import time
import os
import json
import urllib.request

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
LOG_FILE = "/opt/honeyroot/logs/honeypot.json"

def send_alert(event):
    if not WEBHOOK_URL: return
    data = {
        "content": f"🚨 **Malware Captured!**\n**IP:** {event['payload']['ip']}\n**URL:** {event['payload']['url']}\n**SHA256:** {event['payload']['sha256']}"
    }
    req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Failed to send alert: {e}")

def tail_logs():
    with open(LOG_FILE, 'r') as f:
        f.seek(0, 2) # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            try:
                event = json.loads(line)
                if event.get("event_type") == "malware_captured":
                    send_alert(event)
            except json.JSONDecodeError:
                pass

if __name__ == "__main__":
    tail_logs()
