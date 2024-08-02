import flet as ft
import json

def create_player_container(app):

    with open(app.smpl_configs_dir, 'r') as f:
            config_data = json.load(f)
            username = config_data.get('accounts')[0].get('username')
   

    player_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(
                    src=app.player_avatar,
                    width=40,
                    height=40,
                    fit=ft.ImageFit.COVER,
                    border_radius=4
                ),
                ft.Text(
                    username,
                    color=app.colors["WHITE"],
                    size=16,
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.CENTER,
                    font_family="RubikRegular",
                )
            ],
            spacing=8
        ),
        border_radius=8,
        left=902,
        top=8,
        width=226,
        height=56,
        bgcolor=app.colors["DARK_GRAY"],
        alignment=ft.alignment.center_left,
        padding=ft.padding.all(8)
    )

    return player_container
