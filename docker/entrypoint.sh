#!/bin/bash
set -e

echo "[*] Starting HoneyRoot-X..."
# Execute the main server script
exec python core/server.py
