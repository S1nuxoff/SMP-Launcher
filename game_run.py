import os
import json
from subprocess import call, CREATE_NO_WINDOW
from uuid import uuid1
from minecraft_launcher_lib.command import get_minecraft_command
# АРТУР: 6863d279-732f-3906-aafe-2f8a1ca0f7ee

def mc_run(minecraft_dir, mc_version_id, username, memory_allocation):
    version_dir = os.path.join(minecraft_dir, 'versions', mc_version_id)

    if not os.path.exists(version_dir):
        print(f"Version directory '{version_dir}' does not exist.")
        return
    
    options = {
        'username': username,
        'uuid': str(uuid1()),
        'token': '',
        'jvmArguments': [f"-Xmx{memory_allocation}M"]
    }
    print(f"Options: {options}")

    minecraft_command = get_minecraft_command(version=mc_version_id, minecraft_directory=minecraft_dir, options=options)
    print(f"Running command: {' '.join(minecraft_command)}")
    
    call(minecraft_command, creationflags=CREATE_NO_WINDOW)
