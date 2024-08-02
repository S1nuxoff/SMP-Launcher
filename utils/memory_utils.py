# memmory_utils.py
import psutil
import json

def get_available_memory():
    mem = psutil.virtual_memory()
    return mem.total / (1024 ** 3)

def load_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_config(file_path, config_data):
    with open(file_path, 'w') as f:
        json.dump(config_data, f, indent=4)

def get_allocated_memory(config_data, default_value=4096):
    return config_data.get('memory_allocation', default_value) / 1024

def set_allocated_memory(config_data, value):
    config_data['memory_allocation'] = int(value * 1024)
