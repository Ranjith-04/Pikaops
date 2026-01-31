import os
import platform
import shlex

def launch_ssh_session(user: str, ip: str, port: int = 22):
    """
    Constructs and executes the SSH command to connect to a remote server.
    Handles command injection safety and OS-specific execution.
    """
    # Sanitize inputs
    safe_user = shlex.quote(user)
    safe_ip = shlex.quote(ip)
    
    # Build SSH command
    cmd = f"ssh {safe_user}@{safe_ip} -p {port}"
    
    print(f"--- Connecting to {safe_user}@{safe_ip} ---")
    
    try:
        # Windows handling involves some nuances with os.system vs subprocess,
        # but for a TUI release where we want to take over the console, 
        # os.system is often the most reliable "take over terminal" method.
        if platform.system() == "Windows":
            # Extra basic check for Windows since shlex is POSIX-focused
            if any(c in ip for c in "&|;<>"):
                print("Security Warning: Invalid characters in IP address.")
                return
            os.system(cmd)
        else:
            os.system(cmd)
            
    except Exception as e:
        print(f"SSH Launch Failed: {e}")
    
    print("\n--- Session End ---")
