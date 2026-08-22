import socket
import sys

def check_health(host="127.0.0.1", port=2222):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        
        # Expect the SSH banner
        banner = sock.recv(1024).decode('utf-8')
        sock.close()
        
        if "SSH-2.0-paramiko" in banner:
            sys.exit(0) # Healthy
        else:
            sys.exit(1) # Unhealthy banner
    except Exception:
        sys.exit(1) # Connection failed

if __name__ == "__main__":
    check_health()
