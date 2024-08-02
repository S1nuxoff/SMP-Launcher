import flet as ft
from utils.update_checker import update

def create_update_modal(page: ft.Page, app, latest_version):
    def handle_close(e):
        try:
            page.close(dlg_modal)
            page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))
        except Exception as error:
            print(f"Error closing modal: {error}")

    def handle_download(e):
        try:
            e.control.text = "Updating..."  # Change the button text
            e.control.disabled = True  # Disable the button
            e.control.style.bgcolor = app.colors["BLUE"]  # Change background color
            e.control.update()  # Update the button to reflect the new state
            update(page, app.storage_path, app.new_version)  # Call the update function
        except Exception as error:
            print(f"Error during update: {error}")

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Image(src="https://static-00.iconduck.com/assets.00/rocket-emoji-2048x2018-qczjidkx.png", width=100, height=100),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Update your app", size=24, font_family="RubikMedium", weight=ft.FontWeight.BOLD, color=app.colors["WHITE"]),
                    ft.Text("SMPlauncher " + latest_version, weight=ft.FontWeight.BOLD, color=app.colors["GREEN"], size=18),

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            width=300,
            height=100,
            border_radius=15,
        ),
        actions=[
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "Update",
                        on_click=handle_download,  # Use the handle_download function
                        width=268, height=40,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5),
                            padding=0,
                            bgcolor=app.colors["GREEN"],
                            color=app.colors["WHITE"],
                        ),
                    ),
                    ft.TextButton(
                        "Ignore",
                        on_click=handle_close,
                        style=ft.ButtonStyle(color=app.colors["WHITE"]),
                    ),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        on_dismiss=lambda e: page.add(
            ft.Text("Modal dialog dismissed", color=app.colors["GRAY"]),
        ),
        shape=ft.RoundedRectangleBorder(radius=16),
        bgcolor=app.colors["DARK_GRAY"],
    )
    return dlg_modal
