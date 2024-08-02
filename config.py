import os
import json
from minecraft_launcher_lib.utils import get_minecraft_directory

def get_config_path():
    smpl_dir = get_minecraft_directory().replace('minecraft', 'smplauncher')
    return os.path.join(smpl_dir, "smplauncher.json")

def load_config():
    config_path = get_config_path()
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config: {e}")
        return {}

CONFIG = load_config()
