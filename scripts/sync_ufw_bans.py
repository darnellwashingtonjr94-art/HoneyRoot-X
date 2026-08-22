import json
import subprocess
import time

LOG_FILE = "../logs/honeypot.json"
BANNED_IPS = set()

def ban_ip(ip):
    if ip not in BANNED_IPS:
        print(f"[*] Banning IP via UFW: {ip}")
        subprocess.run(["ufw", "deny", "from", ip], capture_output=True)
        BANNED_IPS.add(ip)

def tail_and_ban():
    with open(LOG_FILE, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            try:
                event = json.loads(line)
                if event.get("event_type") == "connection":
                    ban_ip(event["payload"]["ip"])
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    tail_and_ban()
