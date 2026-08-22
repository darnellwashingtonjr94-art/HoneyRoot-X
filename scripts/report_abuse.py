import json
import os
import urllib.request
import urllib.parse

ABUSEIPDB_API_KEY = os.environ.get("ABUSEIPDB_API_KEY")
LOG_FILE = "../logs/honeypot.json"
REPORTED_IPS_FILE = "../logs/reported_ips.txt"

def report_ip(ip, categories="18,22"): # 18 = Brute Force, 22 = SSH
    if not ABUSEIPDB_API_KEY: return
    
    url = "https://api.abuseipdb.com/api/v2/report"
    data = urllib.parse.urlencode({
        'ip': ip,
        'categories': categories,
        'comment': 'Automated report from HoneyRoot-X SSH Honeypot: SSH Brute Force/Payload Delivery'
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    })
    
    try:
        urllib.request.urlopen(req)
        print(f"[+] Successfully reported {ip} to AbuseIPDB")
    except Exception as e:
        print(f"[-] Failed to report {ip}: {e}")

def main():
    reported = set()
    if os.path.exists(REPORTED_IPS_FILE):
        with open(REPORTED_IPS_FILE, "r") as f:
            reported = set(f.read().splitlines())

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
                if event.get("event_type") == "auth_attempt":
                    ip = event["payload"]["ip"]
                    if ip not in reported:
                        report_ip(ip)
                        reported.add(ip)
                        with open(REPORTED_IPS_FILE, "a") as rf:
                            rf.write(f"{ip}\n")
            except Exception:
                continue

if __name__ == "__main__":
    main()
