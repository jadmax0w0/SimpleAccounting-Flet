import ui
import data
import flet as ft
from flet import Page

def main(page: Page):
    page.title = "Simple Accounting"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    app = data.load_app()  # TODO: use save_json

    import random
    import utils as U
    for _ in range(50):
        app.append_item(
            type=random.choice(U.AccountItemTypes.CustomTypes),
            name="",
            amount=random.randrange(10, 200),
            time=U.random_datetime(year=(2024, 2025)),
        )
    
    appui = ui.AccountingAppUI(backend=app)  # 在创建 ui 模块前，先把后端初始化、读取之类的工作处理好
    safe = ft.SafeArea(content=appui, expand=True)

    page.add(safe)

    appui.update()


if __name__ == "__main__":
    ft.app(target=main)