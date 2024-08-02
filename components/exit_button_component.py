import flet as ft

def create_exit_button(app):
    def on_exit_click(e):
        try:
            app.logout()
            print("User logged out successfully.")
        except Exception as error:
            print(f"Error during logout: {error}")

    exit_button = ft.Container(
        width=56,
        height=56,
        border_radius=8,
        right=24,
        top=8,
        bgcolor=app.colors["DARK_GRAY"],
        padding=ft.padding.all(8),
        content=ft.IconButton(
            icon=ft.icons.LOGOUT,
            icon_color=app.colors["WHITE"],
            icon_size=16,
            on_click=on_exit_click
        )
    )

    return exit_button
