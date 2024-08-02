import os
import zipfile
import json
import subprocess
from utils.firebase_init import db, bucket, smpl_dir, smpl_configs_dir, firestore

def load_config():
    try:
        with open(smpl_configs_dir, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {smpl_configs_dir}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from config file: {e}")
        return {}

config_data = load_config()
current_version = config_data.get('version', '0.0.0')

temp_dir = os.path.join(smpl_dir, 'temp')
temp_launcher_dir = os.path.join(temp_dir, 'SMPlauncher')
updater = os.path.join(smpl_dir, 'updater.exe')

def download_and_extract_file(new_version, page, storage_path, extract_to):
    try:
        config_data['version'] = new_version
        with open(smpl_configs_dir, 'w') as f:
            json.dump(config_data, f)
        
        blob = bucket.blob(storage_path)
        os.makedirs(temp_dir, exist_ok=True)
        local_filename = os.path.join(smpl_dir, os.path.basename(storage_path))
        
        print(f"Downloading {storage_path} to {local_filename}")
        blob.download_to_filename(local_filename)
        
        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
            print(f"Extracting {local_filename} to {temp_dir}")
            zip_ref.extractall(temp_dir)
        os.remove(local_filename)
        page.window.close()
        
        if os.path.exists(updater):
            subprocess.Popen([updater])
            print("Updater started successfully.")
        else:
            print(f"Updater file not found: {updater}")
        
        os._exit(0)
    except Exception as e:
        print(f"Error during download and extraction: {e}")
        os._exit(1)

def check_for_updates():
    try:
        updates_ref = db.collection('updates').order_by('version', direction=firestore.Query.DESCENDING).limit(1)
        docs = updates_ref.stream()
        
        for doc in docs:
            update_data = doc.to_dict()
            latest_version = update_data['version']
            storage_path = update_data['storage_path']
            
            if latest_version > current_version:
                return True, storage_path, latest_version
        return False, None, None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False, None, None

def update(page, storage_path, new_version):
    if storage_path and new_version:
        download_and_extract_file(new_version, page, storage_path, smpl_dir)
        print(f"Update to version {new_version} completed.")
