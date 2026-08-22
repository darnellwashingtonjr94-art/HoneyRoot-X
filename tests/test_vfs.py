import pytest
from core.fake_shell import VirtualFileSystem

def test_vfs_resolve_path():
    vfs = VirtualFileSystem()
    
    # Test absolute
    assert vfs.resolve_path("/etc/passwd") == "/etc/passwd"
    
    # Test relative from /root
    vfs.cwd = "/root"
    assert vfs.resolve_path("test.txt") == "/root/test.txt"
    
    # Test relative from root (/)
    vfs.cwd = "/"
    assert vfs.resolve_path("tmp") == "/tmp"
