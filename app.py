import ui
import data
import flet as ft
from flet import Page

def main(page: Page):
    page.title = "Simple Accounting"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    app = data.AccountingApp()
    appui = ui.AccountingAppUI(backend=app)

    import random
    import utils as U
    for _ in range(50):
        app.append_item(
            type=random.choice(U.AccountItemTypes.CustomTypes),
            name="",
            amount=random.randrange(10, 200),
            time=U.random_datetime(year=False),
        )

    page.add(appui)
    appui.ui_build()


if __name__ == "__main__":
    ft.app(target=main)