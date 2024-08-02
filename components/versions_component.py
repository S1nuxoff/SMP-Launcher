import flet as ft

def create_versions(app):
    try:
        def update_hero(version_data):
            try:
                app.selected_version = version_data
                app.page.controls.clear()
                from pages.view_main import main_view
                main_view(app.page, app)
            except Exception as e:
                print(f"Error updating hero: {e}")

        def create_version_container(version_data):
            return ft.Container(
                width=354,
                height=80,
                border_radius=8,
                padding=ft.padding.all(8),
                bgcolor=app.colors["DARK_GRAY"] if version_data == app.selected_version else app.colors["BLACK"],
                content=ft.Row(
                    controls=[
                        ft.Image(
                            src=version_data['icon'],
                            width=64,
                            height=64,
                            fit=ft.ImageFit.COVER,
                            border_radius=8,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(version_data['name'], size=16, color=app.colors["WHITE"], font_family="RubikRegular", width=247),
                                ft.Text(version_data['description'], size=12, color=app.colors["LIGHT_GRAY"], font_family="RubikRegular", width=247),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=16,
                ),
                on_click=lambda e: update_hero(version_data)
            )

        return ft.Container(
            width=354,
            height=367,
            left=902,
            top=89,
            content=ft.Stack(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("SMP Versions", size=24, color=app.colors["WHITE"], weight=ft.FontWeight.W_500, font_family="RubikBold"),
                            *[create_version_container(version) for version in app.versions_list]
                        ],
                        spacing=16,
                        scroll=ft.ScrollMode.ALWAYS
                    )
                ],
            ),
        )
    except Exception as e:
        print(f"Error creating versions container: {e}")
