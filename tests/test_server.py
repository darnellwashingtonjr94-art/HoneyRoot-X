import pytest
import paramiko
from core.server import HoneyServer

def test_auth_password_root():
    server = HoneyServer()
    # The honeypot should accept the root user
    result = server.check_auth_password("root", "anypassword123")
    assert result == paramiko.AUTH_SUCCESSFUL

def test_auth_password_other():
    server = HoneyServer()
    # The honeypot should reject non-root users to force them to keep trying
    result = server.check_auth_password("admin", "admin")
    assert result == paramiko.AUTH_FAILED
