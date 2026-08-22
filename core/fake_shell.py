import time
from logger import log_event

class VirtualFileSystem:
    def __init__(self):
        self.cwd = "/root"
        # Flat dictionary representing absolute paths to files and directories
        self.files = {
            "/etc/passwd": "root:x:0:0:root:/root:/bin/bash\nsshd:x:121:65534::/run/sshd:/usr/sbin/nologin\n",
            "/etc/shadow": "root:$6$rounds=50000$fakesalt$fakehash:18353:0:99999:7:::\n",
            "/root/.bash_history": "apt update\napt upgrade -y\n",
            "/root/flag.txt": "Nice try!\n"
        }
        # Define valid directories to allow 'cd' and 'ls'
        self.directories = ["/", "/etc", "/root", "/var", "/tmp"]

    def resolve_path(self, path):
        if path.startswith("/"):
            return path
        if self.cwd == "/":
            return f"/{path}"
        return f"{self.cwd}/{path}"

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
                    log_event("command_executed", {"ip": attacker_ip, "command": cmd_line})
                    
                    parts = cmd_line.split()
                    cmd = parts[0].lower()
                    
                    # Virtual File System Logic
                    if cmd == "pwd":
                        channel.send(f"{vfs.cwd}\r\n".encode('utf-8'))
                        
                    elif cmd == "cd":
                        target = parts[1] if len(parts) > 1 else "/root"
                        new_dir = vfs.resolve_path(target)
                        if new_dir in vfs.directories:
                            vfs.cwd = new_dir
                        else:
                            channel.send(f"-bash: cd: {target}: No such file or directory\r\n".encode('utf-8'))
                            
                    elif cmd == "cat":
                        if len(parts) > 1:
                            target_file = vfs.resolve_path(parts[1])
                            if target_file in vfs.files:
                                channel.send(vfs.files[target_file].encode('utf-8'))
                            elif target_file in vfs.directories:
                                channel.send(f"cat: {parts[1]}: Is a directory\r\n".encode('utf-8'))
                            else:
                                channel.send(f"cat: {parts[1]}: No such file or directory\r\n".encode('utf-8'))
                        else:
                            channel.send(b"cat: missing operand\r\n")
                            
                    elif cmd == "ls":
                        # Simple ls matching current directory prefix
                        items = []
                        for d in vfs.directories:
                            if d.startswith(vfs.cwd) and d != vfs.cwd:
                                items.append(d.replace(vfs.cwd + "/", "").split("/")[0])
                        for f in vfs.files.keys():
                            if f.startswith(vfs.cwd) and f != vfs.cwd:
                                items.append(f.replace(vfs.cwd + "/", "").split("/")[0])
                        
                        unique_items = sorted(list(set(items)))
                        if unique_items:
                            channel.send(("  ".join(unique_items) + "\r\n").encode('utf-8'))

                    elif cmd == "echo" and len(parts) > 2 and (">" in parts or ">>" in parts):
                        # Naive file write simulation
                        try:
                            redirect_idx = parts.index(">") if ">" in parts else parts.index(">>")
                            text = " ".join(parts[1:redirect_idx]).strip("'\"") + "\n"
                            filename = vfs.resolve_path(parts[redirect_idx + 1])
                            
                            if ">>" in parts and filename in vfs.files:
                                vfs.files[filename] += text
                            else:
                                vfs.files[filename] = text
                        except Exception:
                            channel.send(b"bash: syntax error near unexpected token\r\n")

                    elif cmd == "whoami":
                        channel.send(b"root\r\n")
                    elif cmd == "id":
                        channel.send(b"uid=0(root) gid=0(root) groups=0(root)\r\n")
                    elif cmd == "exit":
                        break
                    else:
                        channel.send(f"-bash: {cmd_line}: command not found\r\n".encode('utf-8'))
                
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
