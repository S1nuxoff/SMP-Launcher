import flet as ft
from utils.authentication import register_user

logo_image_url = "https://i.ibb.co/ph29y2j/s-logo-1.png"

def register_view(page: ft.Page, app):
    initialize_page(page, app)
    error_message = create_error_message_container(app)

    def hide_error_message():
        error_message.visible = False
        error_message.update()

    def show_error_message(message):
        error_message.content.controls[1].controls[1].value = message
        error_message.visible = True
        error_message.update()

    def on_sign_in_click(e):
        email = email_field.value
        password = password_field.value
        username = name_field.value
        try:
            user_id = register_user(email, password, username)
            if user_id:
                # Redirect to main view
                page.go("/main_view")
            else:
                show_error_message("Username already exists or invalid email/password.")
        except ValueError as ve:
            show_error_message(str(ve))
        except Exception as error:
            show_error_message(str(error))

    def sign_in_click(e):
        page.go("/login_view")

    sign_button = create_sign_button(app, on_sign_in_click)
    logo = create_logo()
    left_img = create_left_image()
    text = create_text_column(app)
    email_field, password_field, name_field = create_input_fields(app)
    inputs = ft.Column(
        controls=[
            email_field,
            name_field,
            password_field,
        ],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    right = create_right_column(app, logo, text, inputs, sign_button, sign_in_click)

    page.add(
        ft.Stack(
            width=page.width,
            controls=[
                error_message,
                left_img,
                right,
            ],
        )
    )

def initialize_page(page, app):
    page.title = "SMPlauncher"
    page.bgcolor = app.colors["BLACK"]
    page.window_resizable = False
    page.window_full_screen = False
    page.window_maximizable = False
    page.window_maximized = False
    page.window_center()
    page.fonts = {
        "Rubik": "fonts/Rubik-Regular.ttf",
        'RubikBold': 'fonts/Rubik-Bold.ttf',
        'RubikBlack': 'fonts/Rubik-Black.ttf',
        'RubikMedium': 'fonts/Rubik-Medium.ttf',
        'RubikLight': 'fonts/Rubik-Light.ttf',
        'RubikSemiBold': 'fonts/Rubik-SemiBold.ttf',
        'RubikRegular': 'fonts/Rubik-Regular.ttf',
        'RubikSemiBold': 'fonts/Rubik-SemiBold.ttf',
    }

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

def create_sign_button(app, on_sign_in_click):
    return ft.ElevatedButton(
        text="Sign up",
        bgcolor=app.colors["GREEN"],
        width=328,
        height=56,
        color=app.colors["WHITE"],
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
        on_click=on_sign_in_click
    )

def create_logo():
    return ft.Container(
        content=ft.Image(src=logo_image_url, width=40, height=60),
    )

def create_left_image():
    return ft.Container(
        content=ft.Image(src="https://i.ibb.co/SvDmw0S/login-screen-img.png", width=650, height=650),
        left=70, top=20
    )

def create_text_column(app):
    return ft.Column(
        controls=[
            ft.Text("Let’s get started", font_family="RubikBold", size=32, weight=ft.FontWeight.BOLD, color=app.colors["WHITE"]),
            ft.Text("Create account to use app", font_family="RubikNormal", size=16, text_align=ft.TextAlign.CENTER, color=app.colors["LIGHT_GRAY"]),
        ],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

def create_input_fields(app):
    email_field = ft.TextField(
        label="User Email",
        border_radius=8,
        bgcolor=app.colors["DARK_GRAY"],
        width=328,
        border=ft.border.all(1, app.colors["LIGHT_GRAY"]),
        focused_border_color=app.colors["WHITE"],
    )

    password_field = ft.TextField(
        password=True,
        label="Password",
        border_radius=8,
        bgcolor=app.colors["DARK_GRAY"],
        width=328,
        border=ft.border.all(1, app.colors["LIGHT_GRAY"]),
        focused_border_color=app.colors["WHITE"],
    )
    name_field = ft.TextField(
        label="Nickname",
        border_radius=8,
        bgcolor=app.colors["DARK_GRAY"],
        width=328,
        border=ft.border.all(1, app.colors["LIGHT_GRAY"]),
        focused_border_color=app.colors["WHITE"],
    )
    return email_field, password_field, name_field

def create_right_column(app, logo, text, inputs, sign_button, sign_in_click):
    return ft.Column(
        controls=[
            logo,
            ft.Container(height=36),
            text,
            ft.Container(height=55),
            inputs,
            ft.Container(height=56),
            sign_button,
            ft.Container(height=8),
            ft.Row(
                controls=[
                    ft.Text("Already have an account", size=14, color=app.colors["WHITE"]),
                    ft.TextButton(
                        "Sign in",
                        on_click=sign_in_click,
                        style=ft.ButtonStyle(
                            overlay_color={"": ft.colors.TRANSPARENT},
                            color=app.colors["GREEN"],
                            padding=0
                        )
                    )
                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        top=40,
        right=70,
        spacing=0
    )
