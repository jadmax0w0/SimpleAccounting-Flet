import flet as ft
import fire
from flet import Page, Control
from data import *


class AccountingAppUI(Control):
    """记账软件的前端 UI 部分"""

    def __init__(self, backend: AccountingApp, ref = None, expand = None, expand_loose = None, col = None, opacity = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None):
        super().__init__(ref, expand, expand_loose, col, opacity, tooltip, badge, visible, disabled, data, rtl)

        self.backend = backend

    def ui_account_items(self) -> list[Control]:
        """ TODO: 将当前账本所有项目转换为账单列表的内容 """
        pass

    def ui_switch_book(self):
        """ TODO: 唤出切换账本的菜单 """
        pass

    def build(self):
        self.label_monthlyincome = ft.Text("账本名 x月 +¥888", weight=600, expand=True)
        self.btn_switchbook = ft.FloatingActionButton(icon=ft.Icons.BOOK, on_click=self.ui_switch_book)
        self.row1 = ft.Row(controls=[self.label_monthlyincome, self.btn_switchbook], vertical_alignment=ft.CrossAxisAlignment.CENTER)

        self.listv_items = ft.ListView(controls=self.ui_account_items())
        raise NotImplementedError()