import json
import os

CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
    "servers": [
        # Example format:
        # {"name": "Prod-DB-01", "ip": "192.168.1.10", "user": "admin", "exporter_url": "http://192.168.1.10:9100/metrics"}
    ],
    "theme": "pika"
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

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
