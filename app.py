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
    safe = ft.SafeArea(content=appui, expand=True)

    page.add(safe)

    import random
    import utils as U
    for _ in range(50):
        app.append_item(
            type=random.choice(U.AccountItemTypes.CustomTypes),
            name="",
            amount=random.randrange(10, 200),
            time=U.random_datetime(year=False),
        )

    appui.build()
    appui.update()


if __name__ == "__main__":
    ft.app(target=main)