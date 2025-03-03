# Welcome to Reflex! This file outlines the steps to create a basic app

import reflex as rx

from .pages import index
from .pages import health
from .pages import not_found
from .table import main_table as main

from .api import root
from .api import test

app = rx.App(
        theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="grass"
    ),
)

app.add_page(index)
app.add_page(health)
app.add_page(main)

app.api.add_api_route(
    path="/",
    endpoint=root
)

app.api.add_api_route(
    path="/test",
    endpoint=test
)

not_found_text = "The page you were looking for could not be found"

app.add_custom_404_page(
    title="404 - Page Not Found", 
    description=not_found_text,
    component=not_found(not_found_text)
)

