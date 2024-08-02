# download_modal.py

import flet as ft

def create_download_modal(app):
    try:
        download_modal = ft.Container(
            content=ft.Row(
                controls=[
                   ft.Text("Downloading", font_family="RubikMedium", color=app.colors["WHITE"], size=14, weight=ft.FontWeight.W_400),
                    ft.ProgressRing(width=24, height=24, color=app.colors["GREEN"], bgcolor=app.colors["DARK_GRAY"]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            width=180,
            height=56,
            border_radius=28,
            bgcolor=app.colors["DARK_GRAY"],
            top=24,
            left=553,
            padding=16,
            animate_position=ft.Animation(1000, "easeInOut"),
            animate_opacity=ft.Animation(1000, "easeInOut"),
            opacity=0,
        )
        return download_modal
    except Exception as e:
        print(f"Error creating download modal: {e}")
