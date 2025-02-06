import flet as ft
from data import *
from utils import *
from uiparts.config import UIConfig

from uiparts.typeslist import ItemTypesList
from uiparts.itemlist import AccountItemList


class TitleCard(ft.Card):

    def __init__(self, backend: AccountingApp, content = None, margin = None, elevation = None, color = None, shadow_color = None, surface_tint_color = None, shape = None, clip_behavior = None, is_semantic_container = None, show_border_on_foreground = None, variant = None, ref = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, key = None, adaptive = None):
        super().__init__(content, margin, elevation, color, shadow_color, surface_tint_color, shape, clip_behavior, is_semantic_container, show_border_on_foreground, variant, ref, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, key, adaptive)
        self.backend = backend

        self.book_title = ft.Text(value=self.backend.current_book.name, text_align=ft.TextAlign.LEFT, size=UIConfig.BookTitleTextSize, weight=UIConfig.BookTitleTextWeight, expand=True)
        self.year_info = ft.Text(value=f"{datetime.now().year} 年", text_align=ft.TextAlign.LEFT, size=UIConfig.TitleYearTextSize, weight=UIConfig.TitleMonthTextWight, expand=2)
        self.filtered_types_info = ft.Text(text_align=ft.TextAlign.RIGHT, size=UIConfig.TitleYearTextSize, weight=UIConfig.TitleMonthTextWight, expand=3)
        self.month_info = ft.Text(value=f"{datetime.now().month} 月", text_align=ft.TextAlign.LEFT, size=UIConfig.TitleMonthTextSize, weight=UIConfig.TitleMonthTextWight, expand=UIConfig.TitleMonthTextExpand)
        self.month_inout = ft.Text(value=self.backend.inout_monthly(to_info=True), text_align=ft.TextAlign.RIGHT, size=UIConfig.TitleInoutTextSize, weight=UIConfig.TitleInoutTextWeight, expand=UIConfig.TitleInoutTextExpand)
        self.switch_books_button = ft.FloatingActionButton(icon=ft.Icons.BOOK, on_click=self.switch_book)

        self.row_year = ft.Row(controls=[self.year_info, self.filtered_types_info], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=UIConfig.TitleRowSpacing, expand=True)
        self.row_month = ft.Row(controls=[self.month_info, self.month_inout], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=UIConfig.TitleRowSpacing, expand=True)
        self.col_month = ft.Column(controls=[self.row_year, self.row_month], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=15, expand=True)
        self.row_bottom = ft.Row(controls=[self.col_month, self.switch_books_button], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, expand=True)

        self.col_title = ft.Column(controls=[self.book_title, self.row_bottom], horizontal_alignment=ft.CrossAxisAlignment.START, expand=True)
        self.container = ft.Container(content=self.col_title, padding=UIConfig.TitleCardInnerPadding, expand=True)
        self.content = self.container

        self.width = UIConfig.TitleCardWidth
        self.height = UIConfig.TitleCardHeight

    def switch_book(self):
        """ TODO: 唤出切换账本的菜单 """
        pass

    def update(self):
        super().update()
        self.content.update()
        print(f"{self.__class__.__name__} updated")

    def filtered_monthly_inout(self, sender):
        ui_item_list, ui_types = sender
        if not isinstance(ui_item_list, AccountItemList) or not isinstance(ui_types, ItemTypesList):
            return
        types = ""
        for t in ui_types.selected_types:
            types += t.icon + " "
        self.filtered_types_info.value = types
        self.month_inout.value = self.backend.addup(key=BookItemSelectKeys.SpecificMonth, to_info=True, items_list=ui_item_list.visible_items)
        self.update()