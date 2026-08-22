#!/bin/bash
# Must be run as root on the host machine
set -e

echo "[*] Moving real SSH daemon to port 2222..."
sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config
sed -i 's/^Port 22/Port 2222/' /etc/ssh/sshd_config

echo "[*] Restarting SSHD..."
systemctl restart sshd

echo "[+] Host prepared! Your real SSH is now on 2222."
echo "    WARNING: Update your firewall rules and DO NOT disconnect your current session yet!"
