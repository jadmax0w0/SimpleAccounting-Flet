import flet as ft
from flet import Page, Control
from data import *


class UIConfig:
    # title card
    BookTitleTextSize = 25
    BookTitleTextWeight = ft.FontWeight.W_600

    TitleMonthTextSize = 15
    TitleMonthTextWight = ft.FontWeight.W_500
    TitleMonthTextWidth = 300
    TitleMonthTextExpand = 3

    TitleInoutTextSize = 15
    TitleInoutTextWeight = ft.FontWeight.W_600
    TitleInoutTextExpand = 2

    TitleColumnSpacing = 15
    TitleRowSpacing = 15

    TitleCardWidth = 500
    TitleCardHeight = 150
    TitleCardInnerPadding = 20
    
    # item list
    ItemTextSize = 15
    ItemTextWeight = ft.FontWeight.W_400
    ItemIconWidth = 20
    ItemNameWidth = 150
    ItemAmountWidth = 100

    ItemListSpacing = 15
    ItemListWidth = 500


class TitleCard(ft.Card):
    def __init__(self, backend: AccountingApp, content = None, margin = None, elevation = None, color = None, shadow_color = None, surface_tint_color = None, shape = None, clip_behavior = None, is_semantic_container = None, show_border_on_foreground = None, variant = None, ref = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, key = None, adaptive = None):
        super().__init__(content, margin, elevation, color, shadow_color, surface_tint_color, shape, clip_behavior, is_semantic_container, show_border_on_foreground, variant, ref, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, key, adaptive)
        self.backend = backend

    def switch_book(self):
        """ TODO: 唤出切换账本的菜单 """
        pass

    def build(self):
        super().build()
        book_title = ft.Text(value=self.backend.current_book.name, text_align=ft.TextAlign.LEFT, size=UIConfig.BookTitleTextSize, weight=UIConfig.BookTitleTextWeight, expand=True)
        month_info = ft.Text(value=f"{datetime.now().month} 月", text_align=ft.TextAlign.LEFT, size=UIConfig.TitleMonthTextSize, weight=UIConfig.TitleMonthTextWight, expand=UIConfig.TitleMonthTextExpand)
        month_inout = ft.Text(value=self.backend.inout_monthly(to_info=True), text_align=ft.TextAlign.RIGHT, size=UIConfig.TitleInoutTextSize, weight=UIConfig.TitleInoutTextWeight, expand=UIConfig.TitleInoutTextExpand)
        switch_books_button = ft.FloatingActionButton(icon=ft.Icons.BOOK, on_click=self.switch_book)
        row_month = ft.Row(controls=[month_info, month_inout, switch_books_button], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=UIConfig.TitleRowSpacing, expand=True)
        col_title = ft.Column(controls=[book_title, row_month], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=UIConfig.TitleColumnSpacing, expand=True)
        container = ft.Container(content=col_title, padding=UIConfig.TitleCardInnerPadding, expand=True)

        self.content = container
        self.width = UIConfig.TitleCardWidth
        self.height = UIConfig.TitleCardHeight
        print(f"{self.__class__.__name__} built")

    def update(self):
        super().update()
        self.content.update()
        print(f"{self.__class__.__name__} updated")


class AccountItemList(ft.ListView):
    def __init__(self, backend: AccountingApp, controls = None, horizontal = None, spacing = None, item_extent = None, first_item_prototype = None, divider_thickness = None, padding = None, clip_behavior = None, semantic_child_count = None, cache_extent = None, build_controls_on_demand = None, auto_scroll = None, reverse = None, on_scroll_interval = None, on_scroll = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(controls, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding, clip_behavior, semantic_child_count, cache_extent, build_controls_on_demand, auto_scroll, reverse, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, adaptive)
        self.backend = backend

    def account_items(self) -> list[Control]:
        """将当前账本所有项目转换为账单列表的内容"""
        def item_text(value: str, width: int = None, expand: bool = None, align = ft.TextAlign.CENTER, color: ft.Colors = None):
            return ft.Text(
                value=value,
                width=width,
                size=UIConfig.ItemTextSize,
                weight=UIConfig.ItemTextWeight,
                text_align=align,
                overflow=ft.TextOverflow.FADE,
                color=color,
                expand=expand,
            )
        
        def item_row(data: AccountItem):
            type_icon = item_text(value=data.type.icon, width=UIConfig.ItemIconWidth)
            title = item_text(value=data.name, width=UIConfig.ItemNameWidth)
            time = item_text(value=data.datetime_info, expand=True)
            amount = item_text(
                value=data.amount_info, width=UIConfig.ItemAmountWidth, align=ft.TextAlign.RIGHT, 
                color=(ft.Colors.GREEN if data.amount >= 0 else ft.Colors.RED)
            )
            return ft.Row(
                controls=[type_icon, title, time, amount],
                expand=True,
            )
        
        ui_items = []
        items = self.backend.current_items()
        for item in items:
            ui_items.append(item_row(item))
        return ui_items

    def build(self):
        super().build()
        self.controls = self.account_items()
        self.spacing = UIConfig.ItemListSpacing
        self.expand = True
        self.width = UIConfig.ItemListWidth
        print(f"{self.__class__.__name__} built")

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")


class MainColumn(ft.Column):
    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)
        self.backend = backend

    def build(self):
        super().build()
        self.title_card = TitleCard(backend=self.backend)
        self.items_list = AccountItemList(backend=self.backend)

        # initializing Column base class
        self.controls = [self.title_card, self.items_list]
        self.expand=True
        self.spacing=UIConfig.ItemListSpacing
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER
        print(f"{self.__class__.__name__} built")

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")


class AccountingAppUI(ft.Container):
    """记账软件的前端 UI 部分"""
    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)
        self.expand = True

        self.backend = backend

    def build(self):
        super().build()
        self.content = MainColumn(self.backend)
        print(f"{self.__class__.__name__} built")

    def update(self):
        super().update()
        self.content.update()
        print(f"{self.__class__.__name__} updated")