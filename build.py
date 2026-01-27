
import os
import shutil
import subprocess
import platform
import sys

def clean():
    """Removes build artifacts."""
    folders = ["build", "dist"]
    files = ["PikaOps.spec"]
    
    print("Cleaning up...")
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Removed {folder}/")
    
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed {file}")

def build_windows():
    """Runs PyInstaller for Windows."""
    print("Building for Windows...")
    
    # Verify PyInstaller is installed
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: PyInstaller not found. Please run: pip install pyinstaller")
        return

    # PyInstaller Command
    # We use default console mode (no --windowed) so the TUI renders in the terminal window.
    separator = ";" if platform.system() == "Windows" else ":"
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--name", "PikaOps",
        f"--add-data", f"tui/styles.tcss{separator}tui",
        "--hidden-import", "textual",
        "main.py"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print("\nBuild Complete! Executable is in dist/PikaOps.exe")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
        return

    # Always clean before build
    clean()
    
    if platform.system() == "Windows":
        build_windows()
    else:
        print(f"Auto-build for {platform.system()} is not yet implemented.")
        print("Please see RELEASE.md for Linux instructions.")

if __name__ == "__main__":
    main()
