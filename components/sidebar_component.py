# sidebar.py

import flet as ft

def create_sidebar(app, start_download):
    def navigate_to(path):
        try:
            app.page.go(path)
            print(f"Navigation to {path} successful.")
        except Exception as error:
            print(f"Error navigating to {path}: {error}")

    return ft.Container(
        width=96,
        height=770,
        border_radius=16,
        left=0,
        top=0,
        content=ft.Column(
            controls=[
                ft.Container(
                    width=48,
                    height=144,
                    bgcolor=app.colors["DARK_GRAY"],
                    border_radius=24,
                    padding=ft.padding.all(0),
                    content=ft.Column(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.HOME_ROUNDED,
                                icon_color=app.colors["BLACK"],
                                bgcolor=app.colors["WHITE"],
                                icon_size=16,
                                width=32,
                                height=32,
                                on_click=lambda e: navigate_to("/")
                            ),
                            ft.IconButton(
                                icon=ft.icons.UPDATE_ROUNDED,
                                icon_color=app.colors["WHITE"],
                                bgcolor=app.colors["GRAY"],
                                icon_size=16,
                                width=32,
                                height=32,
                                on_click=lambda e: navigate_to("/mods_view")
                            ),
                            ft.IconButton(
                                icon=ft.icons.SETTINGS_ROUNDED,
                                icon_color=app.colors["WHITE"],
                                bgcolor=app.colors["GRAY"],
                                icon_size=16,
                                width=32,
                                height=32,
                                on_click=lambda e: navigate_to("/settings")
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
