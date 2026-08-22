import time
from logger import log_event

def handle_shell(channel, attacker_ip):
    channel.send(b"Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n\r\n")
    channel.send(b"root@server:~# ")
    
    command = ""
    while True:
        try:
            char = channel.recv(1).decode('utf-8')
            if not char:
                break
                
            if char in ('\r', '\n'):
                channel.send(b"\r\n")
                if command.strip():
                    log_event("command_executed", {"ip": attacker_ip, "command": command.strip()})
                    
                    cmd_lower = command.strip().lower()
                    if cmd_lower == "whoami":
                        channel.send(b"root\r\n")
                    elif cmd_lower == "id":
                        channel.send(b"uid=0(root) gid=0(root) groups=0(root)\r\n")
                    elif cmd_lower == "uname -a":
                        channel.send(b"Linux server 5.15.0-89-generic #99-Ubuntu SMP x86_64 x86_64 x86_64 GNU/Linux\r\n")
                    elif cmd_lower == "pwd":
                        channel.send(b"/root\r\n")
                    elif cmd_lower == "exit":
                        break
                    else:
                        channel.send(f"-bash: {command.strip()}: command not found\r\n".encode('utf-8'))
                
                command = ""
                channel.send(b"root@server:~# ")
            
            elif char in ('\x08', '\x7f'): # Backspace
                if len(command) > 0:
                    command = command[:-1]
                    channel.send(b'\x08 \x08')
            
            else:
                command += char
                channel.send(char.encode('utf-8'))
                
        except Exception:
            break
            
    channel.close()
