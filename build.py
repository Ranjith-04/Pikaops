
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

def add_to_path_windows(executable_dir):
    """Adds the given directory to the Windows User PATH."""
    import winreg
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
        try:
            path_value, _ = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            path_value = ""
        
        if executable_dir.lower() not in path_value.lower():
            print(f"Adding {executable_dir} to User Path...")
            new_path = f"{path_value};{executable_dir}" if path_value else executable_dir
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
            print("Success! You may need to restart your terminal/system for changes to take effect.")
        else:
            print(f"{executable_dir} is already in PATH.")
        
        winreg.CloseKey(key)
        
        # Notify the system of environment change (optional, might not affect current shell immediately)
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.c_long()
        SendMessageTimeout = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeout(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))
        
    except Exception as e:
        print(f"Failed to add to PATH: {e}")
        print(f"Please manually add {executable_dir} to your Environment Variables.")

def build_windows():
    """Runs PyInstaller for Windows."""
    print("Building for Windows...")
    
    # Verify PyInstaller is installed
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: PyInstaller not found. Please run: pip install pyinstaller")
        return

    # PyInstaller Command
    # We use default console mode (no --windowed) so the TUI renders in the terminal window.
    separator = ";" if platform.system() == "Windows" else ":"
    
    # Run PyInstaller via python module to avoid PATH issues
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--name", "pikacli",
        f"--add-data", f"tui/styles.tcss{separator}tui",
        "--collect-all", "textual",
        "--collect-all", "rich",
        "--hidden-import", "rich._unicode_data",
        "main.py"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    dist_dir = os.path.join(os.getcwd(), "dist")
    print(f"\nBuild Complete! Executable is in {dist_dir}\\pikacli.exe")
    
    # Add to path
    add_to_path_windows(dist_dir)

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
