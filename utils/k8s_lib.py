import asyncio
import os
import subprocess
import signal

# Store active tunnel process globally (simple implementation)
TUNNEL_PROCESS = None

def get_scripts_dir():
    """Returns the absolute path to the k8s scripts directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    start_dir = os.path.join(base_dir, "scripts", "k8s")
    if not os.path.exists(start_dir):
        os.makedirs(start_dir)
    return start_dir

def list_k8s_scripts():
    """Lists all files in scripts/k8s/."""
    d = get_scripts_dir()
    try:
        return [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
    except Exception:
        return []

async def run_script(script_name: str):
    """Executes a script and returns stdout/stderr."""
    script_path = os.path.join(get_scripts_dir(), script_name)
    
    # Determine executor based on extension
    # Basic support for .sh and .py, else try execute directly
    cmd = [script_path]
    if script_name.endswith(".py"):
        cmd = ["python", script_path]
    elif script_name.endswith(".sh"):
        cmd = ["bash", script_path]
        
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode() + stderr.decode()
    except Exception as e:
        return f"Execution failed: {str(e)}"

async def start_tunnel(user: str, ip: str, local_port: int = 6443, remote_port: int = 6443):
    """
    Starts an SSH tunnel in background.
    ssh -L local_port:127.0.0.1:remote_port user@ip -N
    """
    global TUNNEL_PROCESS
    if TUNNEL_PROCESS:
        return False, "Tunnel already active."
        
    cmd = [
        "ssh", "-L", f"{local_port}:127.0.0.1:{remote_port}", 
        f"{user}@{ip}", "-N" # -N means no remote command (just forward)
    ]
    
    try:
        # We don't await communicate() because it blocks until exit.
        # We start it and keep a reference.
        TUNNEL_PROCESS = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE
        )
        return True, "Tunnel process started."
    except Exception as e:
        return False, str(e)

async def stop_tunnel():
    """Stops the active tunnel."""
    global TUNNEL_PROCESS
    if not TUNNEL_PROCESS:
        return False, "No active tunnel."

    try:
        TUNNEL_PROCESS.terminate()
        await TUNNEL_PROCESS.wait()
        TUNNEL_PROCESS = None
        return True, "Tunnel stopped."
    except Exception as e:
        return False, str(e)

def is_tunnel_active():
    global TUNNEL_PROCESS
    return TUNNEL_PROCESS is not None and TUNNEL_PROCESS.returncode is None
