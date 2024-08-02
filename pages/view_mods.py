import flet as ft
from components.hero_component import create_hero
from components.versions_component import create_versions
from components.achievements_component import create_achievements
from components.sidebar_component import create_sidebar
from components.update_modal_component import create_update_modal
from components.light_mode_button_component import create_light_mode_button
from components.exit_button_component import create_exit_button
from components.player_component import create_player_container
from components.download_modal_component import create_download_modal
from utils.firebase import get_folder
from components.error_message import create_error_message_container, show_error_message

def mods_view(page: ft.Page, app):
    try:
        page.title = "SMPlauncher"
        page.window_width = 1316
        page.window_height = 770
        page.bgcolor = app.colors["BLACK"]
        page.window_resizable = False
        page.assets_dir = "assets"
        page.window_full_screen = False
        page.window_center()
        page.window_maximizable = False
        page.window_maximized = False
        page.window.icon = "smpl_logo.ico"

        page.fonts = {
            "Rubik": "fonts/Rubik-Regular.ttf",
            'RubikBold': 'fonts/Rubik-Bold.ttf',
            'RubikBlack': 'fonts/Rubik-Black.ttf',
            'RubikMedium': 'fonts/Rubik-Medium.ttf',
            'RubikLight': 'fonts/Rubik-Light.ttf',
            'RubikSemiBold': 'fonts/Rubik-SemiBold.ttf',
            'RubikRegular': 'fonts/Rubik-Regular.ttf',
            'RubikSemiBold': 'fonts/Rubik-SemiBold.ttf',
        }

        error_message_container = create_error_message_container(app)
        page.add(error_message_container)

        download_modal = create_download_modal(app)
        download_modal.top = -100  # Initially position the modal above the visible area

        def progress_callback(progress):
            download_modal.content.controls[1].value = progress
            page.update()

        def start_download():
            try:
                download_modal.top = 24
                download_modal.opacity = 1
                download_modal.update()
                page.update()
                get_folder(app.selected_version.get('mods_path'), app.local_mods_path, progress_callback)
                download_modal.opacity = 0
                download_modal.update()
                page.update()
            except Exception as e:
                show_error_message(error_message_container, str(e))

        if app.updates_available:
            dlg_modal = create_update_modal(page, app, app.new_version)
            page.open(dlg_modal)

        page.add(
            ft.Stack(
                [   
                    ft.Text("v1.6.3", top=684, left=30, size=12, color=app.colors["LIGHT_GRAY"], weight=ft.FontWeight.W_500, font_family="RubikMedium"),
                    create_hero(app),
                    download_modal,
                    create_sidebar(app, start_download),
                    create_versions(app),
                    create_achievements(app),
                    create_light_mode_button(app),
                    create_exit_button(app),
                    create_player_container(app)
                ]
            )
        )

        page.update()
    except Exception as e:
        show_error_message(error_message_container, str(e))
