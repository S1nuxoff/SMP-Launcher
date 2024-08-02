import os
import zipfile
from minecraft_launcher_lib.utils import get_minecraft_directory
import json
from utils.firebase_init import db, bucket, smpl_dir  # Import necessary objects and paths
from dotenv import load_dotenv

load_dotenv()

def get_files(file_name, local_path):
    try:
        blob = bucket.blob(file_name)
        blob.download_to_filename(local_path)
        print(f"File {file_name} downloaded to {local_path}")
    except Exception as e:
        print(f"Error downloading file {file_name}: {e}")

def extract_zip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"File {zip_path} extracted to {extract_to}")
    except Exception as e:
        print(f"Error extracting file {zip_path}: {e}")

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
        else:
            print(f"File {file_path} does not exist.")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

def get_folder(folder_path, local_folder_path):
    print(folder_path, local_folder_path)
    try:
        blobs = bucket.list_blobs(prefix=folder_path)

        total_files = sum(1 for _ in blobs)  # Count total files
        downloaded_files = 0

        blobs = bucket.list_blobs(prefix=folder_path)  # Recreate iterator

        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)

        for blob in blobs:
            if blob.name.endswith('/'):
                continue
            local_file_path = os.path.join(local_folder_path, os.path.relpath(blob.name, folder_path))
            local_file_dir = os.path.dirname(local_file_path)

            if not os.path.exists(local_file_dir):
                os.makedirs(local_file_dir)

            blob.download_to_filename(local_file_path)
            downloaded_files += 1
            print(f"File {blob.name} downloaded to {local_file_path}")
    except Exception as e:
        print(f"Error downloading folder {folder_path}: {e}")

def get_data(collection_name):
    try:
        docs = db.collection(collection_name).stream()
        return [{**doc.to_dict(), 'id': doc.id} for doc in docs]
    except Exception as e:
        print(f"Error fetching data from collection {collection_name}: {e}")
        return []
