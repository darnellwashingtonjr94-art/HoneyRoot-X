import os
import json

TARGET_DIRS = ["/etc", "/var/log", "/bin"]
OUTPUT_FILE = "fake_fs_dump.json"
MAX_FILE_SIZE = 1024 * 5 # Only read first 5KB of files

def generate_fs_map():
    fs_map = {"files": {}, "directories": ["/"]}
    
    for target in TARGET_DIRS:
        for root, dirs, files in os.walk(target):
            if root not in fs_map["directories"]:
                fs_map["directories"].append(root)
            
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    if os.path.isfile(filepath) and not os.path.islink(filepath):
                        if os.path.getsize(filepath) < MAX_FILE_SIZE:
                            with open(filepath, "r", errors="ignore") as f:
                                fs_map["files"][filepath] = f.read()
                        else:
                            fs_map["files"][filepath] = "[Binary or Large File Data]"
                except Exception:
                    pass

    with open(OUTPUT_FILE, "w") as f:
        json.dump(fs_map, f, indent=2)
    print(f"[+] Successfully mapped {len(fs_map['files'])} files and {len(fs_map['directories'])} directories to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_fs_map()
