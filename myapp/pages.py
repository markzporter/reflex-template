from rxconfig import config
import reflex as rx
from .table import main_table

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


def index() -> rx.Component:
    return rx.fragment(
        rx.vstack(
            rx.heading("Welcome to the Dash App management console", font_size="2em"),
            main_table()
        ),
    )

def health() -> rx.Component:
    return rx.text("healthy")

def not_found(page_text) -> rx.Component:
    return rx.fragment(
            rx.heading(page_text, font_size="2em"),
    )
    
    