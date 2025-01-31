import flet as ft
import fire

def main(page: ft.Page):
    page.add(ft.Text(value="Hello, world!"))

if __name__ == "__main__":
    ft.app(target=main)