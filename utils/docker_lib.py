import asyncio
import shutil
import json

async def list_containers():
    """
    Lists Docker containers using the `docker` CLI.
    Returns a list of dicts: {id, image, name, status, state}
    """
    if not shutil.which("docker"):
        return []

    # Format: ID|Image|Names|Status|State
    # State is usually 'running', 'exited', etc.
    cmd = ["docker", "ps", "-a", "--format", "{{.ID}}|{{.Image}}|{{.Names}}|{{.Status}}|{{.State}}"]
    
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        
        containers = []
        if stdout:
            lines = stdout.decode().strip().splitlines()
            for line in lines:
                parts = line.split("|")
                if len(parts) >= 5:
                    containers.append({
                        "id": parts[0],
                        "image": parts[1],
                        "name": parts[2],
                        "status": parts[3],
                        "state": parts[4]
                    })
        return containers
    except Exception:
        return []

async def manage_container(container_id: str, action: str):
    """
    Performs start, stop, or restart on a container.
    Returns (success: bool, message: str)
    """
    valid_actions = ["start", "stop", "restart"]
    if action not in valid_actions:
        return False, "Invalid action"
        
    cmd = ["docker", action, container_id]
    
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode == 0:
            return True, f"Container {action}ed successfully."
        else:
            return False, stderr.decode().strip()
            
    except Exception as e:
        return False, str(e)
