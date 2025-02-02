import flet as ft
from flet import Page, Control
from data import *


class AccountingAppUI(ft.Column):
    """记账软件的前端 UI 部分"""
    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)

        self.backend = backend
        self.ui_build(initialization=True)

    def ui_account_items(self) -> list[Control]:
        """将当前账本所有项目转换为账单列表的内容"""
        def ui_construct_item(data: AccountItem):
            type_icon = ft.Text(value=data.type.icon, text_align=ft.TextAlign.CENTER, overflow=ft.TextOverflow.VISIBLE)
            title = ft.Text(value=data.name, text_align=ft.TextAlign.CENTER, overflow=ft.TextOverflow.FADE)
            time = ft.Text(value=data.datetime_info, text_align=ft.TextAlign.CENTER, overflow=ft.TextOverflow.FADE)
            amount = ft.Text(value=data.amount_info, text_align=ft.TextAlign.RIGHT, weight=600, overflow=ft.TextOverflow.FADE, color=(ft.Colors.GREEN if data.amount >= 0 else ft.Colors.RED))
            return ft.Column(
                controls=[type_icon, title, time, amount],
                expand=True,
            )
        
        ui_items = []
        items = self.backend.current_items()
        for item in items:
            ui_items.append(ui_construct_item(item))
        return ui_items

    def ui_switch_book(self):
        """ TODO: 唤出切换账本的菜单 """
        pass

    def ui_build(self, initialization: bool = False):
        monthly_income = f"{self.backend.current_book.name}  {datetime.now().month} 月  {self.backend.inout_monthly(to_info=True)}"
        self.label_monthly_income = ft.Text(monthly_income, weight=600, expand=True)
        self.btn_switch_book = ft.FloatingActionButton(icon=ft.Icons.BOOK, on_click=self.ui_switch_book)
        self.row1 = ft.Row(controls=[self.label_monthly_income, self.btn_switch_book], vertical_alignment=ft.CrossAxisAlignment.CENTER)

        self.listv_items = ft.ListView(controls=self.ui_account_items(), expand=True)

        # initializing Column base class
        self.controls = [self.row1, self.listv_items]
        self.expand=True
        self.spacing=15
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER

        if not initialization:
            self.update()