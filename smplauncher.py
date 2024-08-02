import os
import json
import flet as ft
from utils.firebase import get_data, get_folder
from minecraft_launcher_lib.utils import get_minecraft_directory
from utils.update_checker import check_for_updates
from pages.view_login import login_view
from pages.view_settings import settings_view
from pages.view_main import main_view
from pages.view_mods import mods_view
from pages.view_register import register_view
from assets.colors import BLACK, WHITE, GREEN, DARK_GRAY, GRAY, LIGHT_GRAY, RED
from utils.firebase_init import db
from config import CONFIG

class SMPLauncher:

    def __init__(self, page: ft.Page):
        self.page = page
        self.config_data = CONFIG  
        self.init_data()
        self.init_colors()
        self.init_assets()
    
    def init_data(self):
        self.load_versions()
        self.load_achievements()
        self.setup_directories()
        self.check_updates()
        self.is_login = self.check_login_state()
        self.username = self.config_data['accounts'][0]['username']
        self.memory_allocation = self.config_data.get('memory_allocation', 2988)  # Default to 4 if not specified

    def init_colors(self):
        self.colors = {
            "BLACK": BLACK,
            "WHITE": WHITE,
            "GREEN": GREEN,
            "DARK_GRAY": DARK_GRAY,
            "GRAY": GRAY,
            "LIGHT_GRAY": LIGHT_GRAY,
            "RED": RED,
            "BLUE": "BLUE",
            "PURPLE": "PURPLE",
            "ORANGE": "ORANGE",
            "DARK_BLUE": "DARK_BLUE",
        }

    def init_assets(self):
        self.hero_background = "https://i.ibb.co/xjZrGr5/bg-2-0.png"
        self.player_avatar = "https://i.pinimg.com/474x/54/f4/b5/54f4b55a59ff9ddf2a2655c7f35e4356.jpg"

    def check_login_state(self):
        if not self.config_data.get('accounts'):
            return False
        else:
            account = self.config_data['accounts'][0]
            uid = account.get('uid')
            return uid and self.check_user_in_firestore(uid)

    def check_user_in_firestore(self, uid):
        user_doc = db.collection('users').document(uid).get()
        return user_doc.exists

    def load_versions(self):
        self.versions_list = get_data('smp_versions')
        self.selected_version = self.versions_list[1] if self.versions_list else {}

    def load_achievements(self):
        self.achievements_list = get_data('achievements')
        self.recent_achievements = self.achievements_list[:4] if self.achievements_list else []

    def setup_directories(self):
        self.smpl_dir = get_minecraft_directory().replace('minecraft', 'smplauncher')
        self.smpl_configs_dir = os.path.join(self.smpl_dir, "smplauncher.json")
        self.minecraft_dir = os.path.join(self.smpl_dir, 'smp')
        self.local_mods_path = os.path.join(self.minecraft_dir, 'mods')
        self.local_shaders_path = os.path.join(self.minecraft_dir, 'shaderpacks')
        self.local_mods_path = os.path.join(self.minecraft_dir, 'mods')

    def check_updates(self):
        self.updates_available, self.storage_path, self.new_version = check_for_updates()

    def login(self):
        self.page.go("/")

    def route_change(self, e):
        self.page.controls.clear()
        if self.page.route == "/":
            main_view(self.page, self)
        elif self.page.route == "/settings":
            settings_view(self.page, self)
        elif self.page.route == "/register_view":
            register_view(self.page, self)
        elif self.page.route == "/mods_view":
            mods_view(self.page, self)
        else:
            login_view(self.page, self)
        self.page.update()

    def logout(self):
        self.config_data['accounts'] = []
        with open(self.smpl_configs_dir, 'w') as f:
            json.dump(self.config_data, f, indent=4)
        self.page.go("/login")