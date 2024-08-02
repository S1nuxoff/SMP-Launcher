import flet as ft
from components.sidebar_component import create_sidebar
from utils.firebase import get_folder
from utils.memory_utils import get_available_memory, load_config, save_config, get_allocated_memory, set_allocated_memory

def settings_view(page: ft.Page, app):
    try:
        initialize_page(page, app)
        available_memory = get_available_memory()

        config_data = load_config(app.smpl_configs_dir)
        allocated_memory = get_allocated_memory(config_data)
        if allocated_memory < 0.5 or allocated_memory > available_memory:
            allocated_memory = 4

        def update_allocated_memory_label(e):
            allocated_memory_container.controls[1].controls[1].content.value = f"{e.control.value:.2f}GB"
            allocated_memory_container.controls[1].controls[1].content.update()
            set_allocated_memory(config_data, e.control.value)
            save_config(app.smpl_configs_dir, config_data)

        page_title = create_page_title(app)
        allocated_memory_container = create_allocated_memory_container(app, available_memory, allocated_memory, update_allocated_memory_label)
        game_resolution = create_game_resolution_container(app)
        game_settings = create_game_settings_column(app, allocated_memory_container, game_resolution)
        settings_container = create_settings_container(app, page_title, game_settings)

        page.add(
            ft.Stack(
                controls=[
                    create_sidebar(app, get_folder),
                    settings_container
                ],
            )
        )
        page.update()
    except Exception as e:
        print(f"Error in settings_view: {e}")

def initialize_page(page, app):
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

def create_page_title(app):
    return ft.Text(
        "Preferences",
        size=32,
        font_family="RubikBold",
        weight=ft.FontWeight.W_700,
        color=app.colors["WHITE"],
    )

def create_allocated_memory_container(app, available_memory, allocated_memory, update_allocated_memory_label):
    return ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Text('Allocated Memory', size=24, weight=ft.FontWeight.W_500, color=app.colors["WHITE"], font_family="RubikMedium"),
                    ft.Text('How much memory should we allocate to the game instance', size=14, weight=ft.FontWeight.W_400, color=app.colors["LIGHT_GRAY"], font_family="RubikNormal"),
                ],
                spacing=0
            ),
            ft.Row(
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Slider(
                                min=0.5,
                                max=available_memory,
                                value=allocated_memory,
                                width=960,
                                height=16,
                                label="{value}GB",
                                active_color=app.colors["GREEN"],
                                inactive_color=app.colors["DARK_BLUE"],
                                thumb_color=app.colors["WHITE"],
                                on_change=update_allocated_memory_label
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        '0.5',
                                        font_family="RubikLight",
                                        size=12,
                                        color=app.colors["LIGHT_GRAY"],
                                        weight=ft.FontWeight.W_300
                                    ),
                                    ft.Text(
                                        f'{available_memory:.2f}GB',
                                        font_family="RubikLight",
                                        size=12,
                                        color=app.colors["LIGHT_GRAY"],
                                        weight=ft.FontWeight.W_300
                                    )
                                ],
                                width=1000,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ],
                    ),
                    ft.Container(
                        width=86,
                        height=40,
                        border_radius=8,
                        bgcolor=app.colors["DARK_GRAY"],
                        alignment=ft.alignment.center,
                        content=ft.Text(
                            f'{allocated_memory:.2f}GB',
                            font_family="RubikMedium",
                            size=14,
                            color=app.colors["WHITE"],
                        ),
                    )
                ],
                spacing=16,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
        spacing=8
    )

def create_game_resolution_container(app):
    return ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=1104,
            controls=[
                ft.Column(
                    controls=[
                        ft.Text('Game resolution', size=24, weight=ft.FontWeight.W_500, color=app.colors["WHITE"], font_family="RubikMedium"),
                        ft.Text('Set the resolution of the game instance', size=14, weight=ft.FontWeight.W_400, color=app.colors["LIGHT_GRAY"], font_family="RubikNormal"),
                    ],
                    spacing=0
                ),
                ft.Dropdown(
                    width=180,
                    height=56,
                    border=ft.border.all(1, ft.colors.TRANSPARENT),
                    bgcolor=app.colors["DARK_GRAY"],
                    border_radius=8,
                    focused_border_width=0,
                    focused_border_color=ft.colors.TRANSPARENT,
                    options=[
                        ft.dropdown.Option('1920x1080'),
                        ft.dropdown.Option('1280x720'),
                        ft.dropdown.Option('640x360'),
                        ft.dropdown.Option('480x270'),
                    ],
                )
            ]
        )
    )

def create_game_settings_column(app, allocated_memory_container, game_resolution):
    return ft.Column(
        controls=[
            ft.Text('Game Settings', size=14, color=app.colors["LIGHT_GRAY"], font_family="RubikMedium", weight=ft.FontWeight.W_500),
            allocated_memory_container,
            game_resolution,
        ],
        spacing=16,
    )

def create_settings_container(app, page_title, game_settings):
    return ft.Container(
        width=1160,
        height=688,
        left=96,
        top=8,
        border_radius=16,
        content=ft.Column(
            controls=[
                page_title,
                game_settings
            ],
            spacing=20
        ),
        padding=ft.padding.all(40)
    )
