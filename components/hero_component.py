import flet as ft
from launch import launch

def create_hero(app):
    def handle_launch(app):
        try:
            def update_status(status_text):
                launch_button.text = status_text
                app.page.update()

            def update_progress(progress_value):
                progress_bar.value = progress_value / 100
                app.page.update()

            launch_button.disabled = True
            update_status("Initializing the startup...")

            def on_launch_complete():
                launch_button.disabled = False
                update_status("Launch")
                progress_bar.value = 0
                app.page.update()

            launch(app, on_launch_complete, update_status, update_progress)
        except Exception as error:
            print(f"Error during launch: {error}")

    launch_button = ft.ElevatedButton(
        text="Launch",
        bgcolor=app.colors["BLUE"],
        width=243,
        height=65,
        disabled=not app.selected_version.get('released'),
        color=app.colors["WHITE"],
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=lambda e: handle_launch(app)
    )

    progress_bar = ft.ProgressBar(
        width=243,
        height=2,
        color=app.colors["WHITE"],
        bgcolor=ft.colors.TRANSPARENT,
        value=0,
        border_radius=16
    )

    return ft.Container(
        width=790,
        height=447,
        left=96,
        top=8,
        bgcolor=app.colors["DARK_GRAY"],
        image_src=app.hero_background,
        image_fit=ft.ImageFit.COVER,
        border_radius=16,
        padding=ft.padding.all(30),
        border=ft.border.all(1, "#444444"),
        content=ft.Stack(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(app.selected_version.get('release_date'), size=14, color=app.colors["LIGHT_GRAY"], font_family="RubikRegular"),
                                        ft.Text(app.selected_version.get('name'), size=18, color=app.colors["WHITE"], font_family="RubikRegular"),
                                    ],
                                    spacing=8
                                ),
                                ft.Container(height=30),
                                ft.Image(
                                    src=app.selected_version.get('logo'),
                                    height=64,
                                    fit=ft.ImageFit.COVER,
                                    border_radius=16,
                                ),
                                ft.Container(height=20),
                                ft.Text(app.selected_version.get('description'), size=16, color=app.colors["LIGHT_GRAY"], font_family="RubikRegular", width=243),
                                ft.Container(height=5),
                                ft.Container(height=1, expand=True),
                                launch_button,
                                ft.Container(height=4, expand=True),
                                progress_bar
                            ],
                            expand=True 
                        ),
                        ft.Column( 
                            controls=[
                                ft.Container(height=1, expand=True),  # Spacer to push the image to the bottom
                                ft.Image(src=app.selected_version.get('image'), fit=ft.ImageFit.COVER, border_radius=16, animate_opacity=3,)  
                            ],
                            expand=True  
                        ),
                    ],
                    spacing=0
                )
            ],
        ),
        animate_opacity=3,
    )
