import flet as ft

def create_error_message_container(app):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.ERROR, color=app.colors["RED"]),
                ft.Column(
                    controls=[
                        ft.Text("Whoopsie, here's an error message.", color=app.colors["RED"], font_family="RubikMedium", size=14),
                        ft.Text("Please enter a valid email address.", color=app.colors["WHITE"], font_family="RubikMedium", size=12),
                    ],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=16,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        visible=False,
        top=24,
        bgcolor=app.colors["DARK_GRAY"],
        border_radius=16,
        width=328,
        height=88,
        left=457,
        alignment=ft.alignment.center
    )

def show_error_message(error_message_container, message):
    error_message_container.content.controls[1].controls[1].value = message
    error_message_container.visible = True
    error_message_container.update()

def hide_error_message(error_message_container):
    error_message_container.visible = False
    error_message_container.update()
