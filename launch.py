from minecraft_launcher_lib.utils import get_minecraft_directory
import json
import os
import concurrent.futures
from utils.firebase import get_files, extract_zip_file, delete_file, get_folder
from game_run import mc_run
from utils.file_verification import check_files

def launch(app, on_complete, update_status, update_progress):
    app.init_data()

    smpl_dir = app.smpl_dir
    smpl_configs_dir = app.smpl_configs_dir
    minecraft_dir = app.minecraft_dir
    mc_version = app.selected_version.get('mc_version')
    hash_url = app.selected_version.get('hash')
    cloud_path = app.selected_version.get('min_path')
    mods_path = app.selected_version.get('mods_path')
    shaders_path = app.selected_version.get('shaders_path')
    local_mods_path = app.local_mods_path
    local_shaders_path = app.local_shaders_path
    local_path = os.path.join(smpl_dir, os.path.basename(cloud_path))

  
    with open(smpl_configs_dir, 'r') as f:
        config_data = json.load(f)

    username = config_data.get('accounts')[0].get('username')
    memory_allocation = config_data.get('memory_allocation')

    def complete_launch():
        update_status("Launching...")
        update_progress(100)
        mc_run(minecraft_dir, mc_version, username, memory_allocation)
        on_complete()

    update_status("Check files")
    update_progress(10)

    missing_files = check_files(hash_url, minecraft_dir)

    if not missing_files:
        complete_launch()
    else:
        update_status("Downloading files")
        update_progress(30)
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_files = executor.submit(get_files, cloud_path, local_path)
                # future_mods = executor.submit(get_folder, mods_path, local_mods_path)
                # future_shaders = executor.submit(get_folder, shaders_path, local_shaders_path)
                # Wait for all tasks to complete
                future_files.result()
                # future_mods.result()
                # future_shaders.result()
                
        except Exception as e:
            print(f"Error during file download: {e}")
            return
        
        update_status("Unpacking files")
        update_progress(70)
        
        try:
            extract_zip_file(local_path, minecraft_dir)
            delete_file(local_path)
        except Exception as e:
            print(f"Error during file extraction: {e}")
            return
        complete_launch()