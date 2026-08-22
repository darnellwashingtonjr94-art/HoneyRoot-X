# System Architecture

## Component Flow
1. **Docker Container:** HoneyRoot-X runs inside an isolated `python:3.11-slim` container, executing as a non-root user (`honeyuser`).
2. **Paramiko SSHD (`core/server.py`):** Binds to port 2222 (mapped to 22 on the host). It intercepts all auth attempts, applies a randomized 3-7 second tar-pit delay, and accepts the `root` username.
3. **Virtual File System (`core/fake_shell.py`):** An in-memory dictionary acting as the filesystem. It parses incoming bash commands and returns hardcoded Ubuntu 22.04 responses.
4. **Malware Interception:** If `wget` or `curl` is detected, the python backend executes the HTTP request, hashes the payload, optionally queries VirusTotal, and saves the binary to a mounted volume before faking a successful terminal response to the attacker.
5. **Telemetry (`core/logger.py`):** All events are written as structured NDJSON (Newline Delimited JSON) to a host-mounted volume for SIEM ingestion.
