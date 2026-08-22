import threading
import socket
import paramiko
import sys
import time
import random
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
        # 1. Log the attempt immediately
        log_event("auth_attempt", {"username": username, "password": password})
        
        # 2. Tar-pit: Introduce a random delay between 3 and 7 seconds.
        # Randomization makes it look like standard network latency or server load 
        # rather than an intentional honeypot trap.
        delay = random.uniform(3.0, 7.0)
        time.sleep(delay)
        
        # 3. Grant access for the bait user
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

# ... start_server() function remains the same ...
 
