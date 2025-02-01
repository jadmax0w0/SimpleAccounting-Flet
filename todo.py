import flet as ft
import fire


class FletPage:
    def __init__(self):
        self.page: ft.Page = None

    def render(self, page: ft.Page):
        raise NotImplementedError()


class MainPage(FletPage):
    def __init__(self):
        super().__init__()

    def add_todo(self, e):
        self.page.add(ft.Checkbox(label=self.textf_taskname.value))
        self.textf_taskname.value = ""
        self.page.update()

    def render(self, page):
        self.page = page
        self.textf_taskname = ft.TextField(label="What needs to be done?", autofocus=True)
        self.page.add(self.textf_taskname, ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_todo))


if __name__ == "__main__":
    mainpage = MainPage()
    ft.app(target=mainpage.render)