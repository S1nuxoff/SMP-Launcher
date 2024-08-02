import os
import hashlib
import requests

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error calculating hash for file {file_path}: {e}")
        return None

def fetch_files_info(files_info_url):
    try:
        response = requests.get(files_info_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching file info from URL {files_info_url}: {e}")
        return None

def check_files(files_info_url, target_folder):
    files_info = fetch_files_info(files_info_url)
    if files_info is None:
        return []

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    missing_or_invalid_files = []

    for file_info in files_info:
        file_name = file_info['name']
        expected_hash = file_info['hash']
        file_path = os.path.join(target_folder, file_name)

        # Exclude certain files from hash checking
        if any(subdir in file_path.split(os.sep) for subdir in ["mods", "shaderpacks", "versions"]) or file_name in ["servers.dat", "servers.dat_old"]:
            continue

        if os.path.exists(file_path):
            actual_hash = calculate_file_hash(file_path)
            if actual_hash != expected_hash:
                missing_or_invalid_files.append(file_name)
        else:
            missing_or_invalid_files.append(file_name)

    return missing_or_invalid_files
