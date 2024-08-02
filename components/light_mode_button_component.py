import flet as ft

def create_light_mode_button(app):
    def toggle_light_mode(e):
        try:
            app.is_light_mode = not app.is_light_mode
            app.page.bgcolor = app.colors["WHITE"] if app.is_light_mode else app.colors["BLACK"]
            app.page.update()
            print(f"Light mode toggled to: {'ON' if app.is_light_mode else 'OFF'}")
        except Exception as error:
            print(f"Error toggling light mode: {error}")

    light_mode_button = ft.Container(
        width=56,
        height=56,
        border_radius=8,
        right=88,
        top=8,
        bgcolor=app.colors["DARK_GRAY"],
        content=ft.IconButton(
            icon=ft.icons.LIGHT_MODE_ROUNDED,
            icon_color=app.colors["WHITE"],
            icon_size=16,
            on_click=toggle_light_mode
        )
    )

    return light_mode_button
