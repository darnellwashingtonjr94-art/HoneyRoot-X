import time
import os
import urllib.request
import hashlib
from urllib.parse import urlparse
from logger import log_event

PAYLOAD_DIR = "/opt/honeyroot/logs/payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

class VirtualFileSystem:
    def __init__(self):
        self.cwd = "/root"
        self.files = {}
        self.directories = ["/", "/etc", "/root", "/var", "/tmp"]

    def resolve_path(self, path):
        if path.startswith("/"):
            return path
        if self.cwd == "/":
            return f"/{path}"
        return f"{self.cwd}/{path}"

def download_and_store_payload(url):
    """Downloads malware safely, hashes it, and stores it in the log volume."""
    try:
        # 10 second timeout, 10MB max read to prevent DoS
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read(10 * 1024 * 1024) 
            
            sha256_hash = hashlib.sha256(data).hexdigest()
            filename = os.path.basename(urlparse(url).path) or "index.html"
            
            safe_path = os.path.join(PAYLOAD_DIR, f"{sha256_hash}_{filename}")
            with open(safe_path, "wb") as f:
                f.write(data)
                
            return filename, sha256_hash, len(data)
    except Exception as e:
        return None, str(e), 0

def handle_shell(channel, attacker_ip):
    channel.send(b"Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n\r\n")
    
    vfs = VirtualFileSystem()
    prompt = lambda: f"root@server:{'~' if vfs.cwd == '/root' else vfs.cwd}# ".encode('utf-8')
    channel.send(prompt())
    
    command = ""
    while True:
        try:
            char = channel.recv(1).decode('utf-8')
            if not char:
                break
                
            if char in ('\r', '\n'):
                channel.send(b"\r\n")
                if command.strip():
                    cmd_line = command.strip()
                    parts = cmd_line.split()
                    cmd = parts[0].lower()
                    
                    log_event("command_executed", {"ip": attacker_ip, "command": cmd_line})
                    
                    # --- WGET & CURL INTERCEPTION ---
                    if cmd in ("wget", "curl") and len(parts) > 1:
                        # Find the first string that looks like a URL
                        url = next((p for p in parts if p.startswith("http://") or p.startswith("https://")), None)
                        
                        if url:
                            channel.send(f"Connecting to {url}...\r\n".encode('utf-8'))
                            
                            # Download the payload on the backend
                            filename, file_hash, size = download_and_store_payload(url)
                            
                            if filename and size > 0:
                                log_event("malware_captured", {
                                    "ip": attacker_ip,
                                    "url": url,
                                    "sha256": file_hash,
                                    "size_bytes": size
                                })
                                
                                # Fake a successful download output
                                channel.send(f"HTTP request sent, awaiting response... 200 OK\r\n".encode('utf-8'))
                                channel.send(f"Length: {size} ({size/1024:.1f}K) [application/octet-stream]\r\n".format(size).encode('utf-8'))
                                channel.send(f"Saving to: '{filename}'\r\n\r\n".encode('utf-8'))
                                
                                # Register it in the fake file system so 'ls' shows it
                                vfs.files[vfs.resolve_path(filename)] = f"[Binary Data: {file_hash}]"
                            else:
                                channel.send(f"Resolving host... failed: Connection timed out.\r\nwget: unable to resolve host address\r\n".encode('utf-8'))
                        else:
                            channel.send(f"{cmd}: missing URL\r\n".encode('utf-8'))

                    # --- EXISTING VFS COMMANDS ---
                    elif cmd == "pwd":
                        channel.send(f"{vfs.cwd}\r\n".encode('utf-8'))
                    elif cmd == "ls":
                        items = []
                        for f in vfs.files.keys():
                            if f.startswith(vfs.cwd) and f != vfs.cwd:
                                items.append(f.replace(vfs.cwd + "/", "").split("/")[0])
                        if items:
                            channel.send(("  ".join(set(items)) + "\r\n").encode('utf-8'))
                    elif cmd == "whoami":
                        channel.send(b"root\r\n")
                    elif cmd == "exit":
                        break
                    else:
                        channel.send(f"-bash: {cmd}: command not found\r\n".encode('utf-8'))
                
                command = ""
                channel.send(prompt())
            
            elif char in ('\x08', '\x7f'):
                if len(command) > 0:
                    command = command[:-1]
                    channel.send(b'\x08 \x08')
            else:
                command += char
                channel.send(char.encode('utf-8'))
                
        except Exception:
            break
            
    channel.close()

import json
from urllib.error import HTTPError

# Pull the API key from the environment
VT_API_KEY = os.environ.get("VT_API_KEY", "")

def check_virustotal(sha256_hash):
    """Queries VirusTotal for an existing hash analysis."""
    if not VT_API_KEY:
        return {"status": "skipped", "reason": "No API key configured"}

    url = f"https://www.virustotal.com/api/v3/files/{sha256_hash}"
    req = urllib.request.Request(url, headers={'x-apikey': VT_API_KEY})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
            return {
                "status": "found",
                "malicious": stats.get("malicious", 0),
                "undetected": stats.get("undetected", 0),
                "total_engines": sum(stats.values())
            }
    except HTTPError as e:
        if e.code == 404:
            return {"status": "not_found", "message": "Hash not previously seen by VirusTotal"}
        return {"status": "error", "message": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
