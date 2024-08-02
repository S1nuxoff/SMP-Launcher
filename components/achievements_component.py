import flet as ft

def create_achievements(app):
    try:
        def create_achievement_card(achievement):
            try:
                return ft.Container(
                    bgcolor=app.colors["DARK_GRAY"],
                    width=278,
                    height=164,
                    border_radius=8,
                    border=ft.border.all(1, "#444444"),
                    content=ft.Image(
                        src=achievement.get('image'),
                        width=64,
                        height=64,
                        fit=ft.ImageFit.COVER,
                        border_radius=8,
                    )       
                )
            except Exception as e:
                print(f"Error creating achievement card: {e}")
                return ft.Container()  # Return an empty container in case of error

        return ft.Container(
            width=1160,
            height=232,
            border_radius=8,
            top=479,
            right=24,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Weekly news", size=26, color=ft.colors.WHITE, weight=ft.FontWeight.W_500, font_family="RubikBold"),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                icon_color=app.colors["WHITE"],
                                icon_size=16,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        controls=[create_achievement_card(achievement) for achievement in app.recent_achievements],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=16,
                    )
                ],
                spacing=16,
                alignment=ft.MainAxisAlignment.START
            )
        )
    except Exception as e:
        print(f"Error creating achievements container: {e}")
        return ft.Container()  # Return an empty container in case of error
