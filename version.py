import sys
from typing import Tuple

def read_version() -> str:
    try:
        with open('version.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "1.0.0"

def write_version(version: str) -> None:
    with open('version.txt', 'w') as f:
        f.write(version)

def parse_version(version: str) -> Tuple[int, int, int]:
    major, minor, patch = map(int, version.split('.'))
    return major, minor, patch

def format_version(major: int, minor: int, patch: int) -> str:
    return f"{major}.{minor}.{patch}"

def increment_version(version: str, increment_type: str) -> str:
    major, minor, patch = parse_version(version)
    
    if increment_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif increment_type == "minor":
        minor += 1
        patch = 0
    elif increment_type == "patch":
        patch += 1
    else:
        raise ValueError("Invalid increment type. Use 'major', 'minor', or 'patch'")
    
    return format_version(major, minor, patch)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python version_manager.py show")
        print("  python version_manager.py major")
        print("  python version_manager.py minor")
        print("  python version_manager.py patch")
        print("  python version_manager.py set <version>")
        return

    command = sys.argv[1]

    if command == "show":
        print(f"Current version: {read_version()}")
    
    elif command in ["major", "minor", "patch"]:
        current_version = read_version()
        new_version = increment_version(current_version, command)
        write_version(new_version)
        print(f"Version updated from {current_version} to {new_version}")
    
    elif command == "set":
        if len(sys.argv) != 3:
            print("Please specify new version")
            return
        
        new_version = sys.argv[2]
        # Проверка формата версии
        try:
            parse_version(new_version)
            write_version(new_version)
            print(f"Version set to {new_version}")
        except ValueError:
            print("Invalid version format. Use format: X.Y.Z (e.g., 1.2.3)")
    
    else:
        print("Unknown command")

if __name__ == "__main__":
    main() 