import psutil
import httpx

def get_local_metrics():
    """
    Returns a dictionary of standardized local system metrics.
    """
    # CPU
    cpu_pct = psutil.cpu_percent(interval=None) or 0
    
    # RAM
    mem = psutil.virtual_memory()
    used_gb = mem.used / (1024**3)
    total_gb = mem.total / (1024**3)
    
    # Disk
    disk = psutil.disk_usage('/')
    d_used_gb = disk.used / (1024**3)
    d_total_gb = disk.total / (1024**3)
    
    # Network
    net = psutil.net_io_counters()
    net_bytes = net.bytes_sent + net.bytes_recv
    
    return {
        "cpu": cpu_pct,
        "memory": {
            "percent": mem.percent,
            "used_gb": used_gb,
            "total_gb": total_gb
        },
        "disk": {
            "percent": disk.percent,
            "used_gb": d_used_gb,
            "total_gb": d_total_gb
        },
        "network": {
            "bytes_total": net_bytes
        }
    }

async def get_remote_metrics(url: str, timeout: float = 3.0):
    """
    Fetches and parses basic metrics (load1, mem_free) from a remote Prometheus-like exporter.
    Returns a dict with 'status', 'load', 'mem_free' or error details.
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=timeout)
            
            if resp.status_code == 200:
                lines = resp.text.splitlines()
                load1 = "-"
                mem_free_str = "-"
                
                # Parse Load
                try:
                    load1 = next((l for l in lines if l.startswith("node_load1 ")), "0.0").split()[-1]
                except Exception:
                    pass
                    
                # Parse Memory
                try:
                    mem_bytes = next((l for l in lines if l.startswith("node_memory_MemFree_bytes ")), "0").split()[-1]
                    mem_gb = float(mem_bytes) / (1024**3)
                    mem_free_str = f"{mem_gb:.1f} GB"
                except Exception:
                    mem_free_str = "Err"
                
                return {
                    "status": "ONLINE",
                    "status_style": "[green]ONLINE[/]",
                    "load": load1,
                    "mem_free": mem_free_str
                }
            else:
                return {
                    "status": f"HTTP {resp.status_code}",
                    "status_style": f"[yellow]HTTP {resp.status_code}[/]",
                    "load": "-",
                    "mem_free": "-"
                }

    except httpx.ConnectTimeout:
         return {
            "status": "TIMEOUT",
            "status_style": "[red]TIMEOUT[/]",
            "load": "-",
            "mem_free": "-"
        }
    except httpx.ConnectError:
         return {
            "status": "DOWN",
            "status_style": "[red]DOWN[/]",
            "load": "-",
            "mem_free": "-"
        }
    except Exception as e:
         return {
            "status": "ERROR",
            "status_style": "[red]ERROR[/]",
            "error_msg": str(e),
            "load": "-",
            "mem_free": "-"
        }
