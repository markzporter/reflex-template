import reflex as rx
from .models import DashApp
from .queries import get_active_dash_deployments, create_dash_app, delete_dash_app


def form_field(
    label: str, placeholder: str, type: str, name: str, icon: str, default_value: str = ""
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type, default_value=default_value
                ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )


class State(rx.State):
    """The app state."""

    apps: list[DashApp] = []

    def load_entries(self) -> list[DashApp]:
        """Get all apps from Railway."""
        self.apps = get_active_dash_deployments()

    def add_dash_app(self, form_data):
        create_dash_app(form_data['repository'])
        self.load_entries()
        return rx.window_alert(f"App with repo {form_data['repository']} has been added. ")

    def delete_dash_app(self, id: str):
        delete_dash_app(id)
        self.load_entries()
        return rx.window_alert(f"App has been deleted ")


def show_app(dashapp: DashApp):
    """Show a customer in a table row."""

    return rx.table.row(
        rx.table.cell(dashapp.app_name),
        rx.table.cell(rx.link(dashapp.url, href=dashapp.url)),
        rx.table.cell(dashapp.deployment_status),

        rx.table.cell(dashapp.created_at),
        rx.icon_button(
            rx.icon("trash-2", size=22),
            on_click=lambda: State.delete_dash_app(dashapp.service_id),
            size="2",
            variant="solid",
            color_scheme="red",
        ),
    )


def refresh_button() -> rx.Component:

    return rx.icon_button(
        rx.icon("refresh-ccw", size=26),
        on_click=lambda: State.load_entries,
        size="3",
        )


def add_dash_app_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add New Dash App", size="4", display=[
                        "none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="users", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Dash app",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Add the dash app repo",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Repository
                        form_field(
                            "repository",
                            "markzporter/IMBD-Dashboard",
                            "text",
                            "repository",
                            "user",
                        ),
                    ),

                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Submit App"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.add_dash_app,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def main_table() -> rx.Component:
    return rx.fragment(
        rx.flex(
            add_dash_app_button(),
            refresh_button(),
            rx.spacer(),
        ),

        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Name", "user"),
                    _header_cell("URL", "link"),
                    _header_cell("Deployment Status", "plus"),
                    _header_cell("Created At", "file-clock"),

                ),
            ),
            rx.table.body(rx.foreach(State.apps, show_app)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=State.load_entries,
        ),
    )
