import flet as ft
from smplauncher import SMPLauncher

def main(page: ft.Page):
    try:
        app = SMPLauncher(page)
        page.on_route_change = app.route_change

        # Check the login state and set the initial route
        page.go("/" if app.is_login else "/login")
    except Exception as e:
        print(f"Error initializing the application: {e}")

if __name__ == "__main__":
    ft.app(target=main)
