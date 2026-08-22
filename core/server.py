import threading
import socket
import paramiko
import sys
from fake_shell import handle_shell
from logger import log_event

class HoneyServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        log_event("auth_attempt", {"username": username, "password": password})
        if username == "root":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

def start_server(port=2222, key_file="/opt/honeyroot/host_rsa_key"):
    host_key = paramiko.RSAKey(filename=key_file)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', port))
        sock.listen(100)
        log_event("system_start", {"message": f"HoneyRoot-X listening on port {port}"})
    except Exception as e:
        print(f"[-] Bind failed: {e}")
        sys.exit(1)

    while True:
        client, addr = sock.accept()
        log_event("connection", {"ip": addr[0], "port": addr[1]})
        
        transport = paramiko.Transport(client)
        transport.add_server_key(host_key)
        
        server = HoneyServer()
        try:
            transport.start_server(server=server)
        except paramiko.SSHException:
            continue

        channel = transport.accept(20)
        if channel is None:
            continue

        server.event.wait(10)
        if not server.event.is_set():
            continue

        t = threading.Thread(target=handle_shell, args=(channel, addr[0]))
        t.start()

if __name__ == "__main__":
    start_server()
