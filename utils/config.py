import json
import os
import copy

CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
    "servers": [
        # Example format:
        # {"name": "Prod-DB-01", "ip": "192.168.1.10", "user": "admin", "exporter_url": "http://192.168.1.10:9100/metrics"}
    ],
    "theme": "pika"
}

_cached_config = None
_last_mtime = 0

def load_config():
    global _cached_config, _last_mtime

    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return copy.deepcopy(DEFAULT_CONFIG)
    
    try:
        current_mtime = os.path.getmtime(CONFIG_PATH)
        if _cached_config is not None and current_mtime == _last_mtime:
            return copy.deepcopy(_cached_config)

        with open(CONFIG_PATH, "r") as f:
            _cached_config = json.load(f)
            _last_mtime = current_mtime
            return copy.deepcopy(_cached_config)
    except Exception:
        return copy.deepcopy(DEFAULT_CONFIG)

def save_config(config):
    global _cached_config, _last_mtime

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    _cached_config = copy.deepcopy(config)
    try:
        _last_mtime = os.path.getmtime(CONFIG_PATH)
    except OSError:
        _last_mtime = 0

def add_server(name, ip, user, exporter_url):
    config = load_config()
    config["servers"].append({
        "name": name,
        "ip": ip,
        "user": user,
        "exporter_url": exporter_url
    })
    save_config(config)

def remove_server(name):
    config = load_config()
    config["servers"] = [s for s in config["servers"] if s["name"] != name]
    save_config(config)
