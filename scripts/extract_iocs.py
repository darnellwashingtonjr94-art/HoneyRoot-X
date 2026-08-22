import json
import sys

LOG_FILE = "../logs/honeypot.json"

def extract():
    ips, urls, hashes = set(), set(), set()
    
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                event = json.loads(line.strip())
                payload = event.get('payload', {})
                
                if 'ip' in payload:
                    ips.add(payload['ip'])
                if event.get('event_type') == 'malware_captured':
                    urls.add(payload.get('url'))
                    hashes.add(payload.get('sha256'))
                    
        print(f"--- Extracted {len(ips)} Unique IPs ---")
        for ip in list(ips)[:10]: print(ip)
        
        print(f"\n--- Extracted {len(urls)} Malware URLs ---")
        for url in urls: print(url)
        
        print(f"\n--- Extracted {len(hashes)} SHA256 Hashes ---")
        for h in hashes: print(h)
        
    except FileNotFoundError:
        print(f"Log file not found at {LOG_FILE}")

if __name__ == "__main__":
    extract()
