import flet as ft
from flet import Page, Control
from data import *
import utils as U
from typing import Callable


class UIConfig:
    # title card
    BookTitleTextSize = 25
    BookTitleTextWeight = ft.FontWeight.W_600

    TitleMonthTextSize = 15
    TitleMonthTextWight = ft.FontWeight.W_500
    TitleMonthTextWidth = 300
    TitleMonthTextExpand = 3

    TitleTypesTextExpand = 4
    TitleInoutTextSize = 15
    TitleInoutTextWeight = ft.FontWeight.W_600
    TitleInoutTextExpand = 2

    TitleColumnSpacing = 15
    TitleRowSpacing = 15

    TitleCardWidth = None
    TitleCardHeight = 175
    TitleCardInnerPadding = 20
    
    # item list
    ItemTextSize = 15
    ItemTextWeight = ft.FontWeight.W_400
    ItemIconWidth = 20
    ItemNameWidth = 150
    ItemAmountWidth = 100

    ItemListPadding = 15
    ItemListSpacing = 15
    ItemListWidth = None

    # bottom bar
    TypesListHeight = 30
    TypesListSpacing = 15
    TypeButtonWidth = 50
    TypeButtonColor = ft.Colors.PRIMARY, ft.Colors.PRIMARY_CONTAINER
    TypeButtonColorSelected = ft.Colors.ON_PRIMARY, ft.Colors.ON_PRIMARY_CONTAINER
    BottomRowWidth = None
    BottomRowHeight = 60
    CreateItemButtonWidth = 60
    CreateItemButtonHeight = 60


class UIMessage:
    def __init__(self):
        self.subs: list[Callable[[object], None]] = []

    def add(self, *subscribers: Callable[[object], None]):
        for s in subscribers:
            if s not in self.subs:
                self.subs.append(s)

    def remove(self, subscriber: Callable[[object], None]):
        if subscriber in self.subs:
            self.subs.remove(subscriber)
    
    def invoke(self, sender: object):
        for s in self.subs:
            s(sender)


class TitleCard(ft.Card):
    def __init__(self, backend: AccountingApp, content = None, margin = None, elevation = None, color = None, shadow_color = None, surface_tint_color = None, shape = None, clip_behavior = None, is_semantic_container = None, show_border_on_foreground = None, variant = None, ref = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, key = None, adaptive = None):
        super().__init__(content, margin, elevation, color, shadow_color, surface_tint_color, shape, clip_behavior, is_semantic_container, show_border_on_foreground, variant, ref, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, key, adaptive)
        self.backend = backend

        self.book_title = ft.Text(value=self.backend.current_book.name, text_align=ft.TextAlign.LEFT, size=UIConfig.BookTitleTextSize, weight=UIConfig.BookTitleTextWeight, expand=True)
        self.month_info = ft.Text(value=f"{datetime.now().month} 月", text_align=ft.TextAlign.LEFT, size=UIConfig.TitleMonthTextSize, weight=UIConfig.TitleMonthTextWight, expand=UIConfig.TitleMonthTextExpand)
        self.filtered_types_info = ft.Text(text_align=ft.TextAlign.RIGHT, size=UIConfig.TitleMonthTextSize, weight=UIConfig.TitleMonthTextWight, expand=True)
        self.month_inout = ft.Text(value=self.backend.inout_monthly(to_info=True), text_align=ft.TextAlign.RIGHT, size=UIConfig.TitleInoutTextSize, weight=UIConfig.TitleInoutTextWeight, expand=UIConfig.TitleInoutTextExpand)
        self.switch_books_button = ft.FloatingActionButton(icon=ft.Icons.BOOK, on_click=self.switch_book)

        self.row_month = ft.Row(controls=[self.month_info, self.month_inout], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=UIConfig.TitleRowSpacing, expand=True)
        self.col_month = ft.Column(controls=[self.filtered_types_info, self.row_month], horizontal_alignment=ft.CrossAxisAlignment.END, spacing=15, expand=True)
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
        self.month_inout.value = self.backend.addup(key=BookItemSelectKeys.SpecificMonth, to_info=True, item_list=ui_item_list.visible_items)
        self.update()


class AccountItemList(ft.ListView):
    def __init__(self, backend: AccountingApp, controls = None, horizontal = None, spacing = None, item_extent = None, first_item_prototype = None, divider_thickness = None, padding = None, clip_behavior = None, semantic_child_count = None, cache_extent = None, build_controls_on_demand = None, auto_scroll = None, reverse = None, on_scroll_interval = None, on_scroll = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(controls, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding, clip_behavior, semantic_child_count, cache_extent, build_controls_on_demand, auto_scroll, reverse, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, adaptive)
        self.backend = backend
        
        self.message_pub = UIMessage()
        self.visible_items: list[Control] = backend.current_items(sort_key=BookItemSortKeys.Time)
        self.visible_items_ui = self._parse_ui_items(self.visible_items)
        self.controls = self.visible_items_ui

        self.padding = UIConfig.ItemListPadding
        self.spacing = UIConfig.ItemListSpacing
        self.expand = True
        self.width = UIConfig.ItemListWidth

    def _parse_ui_items(self, items: list[AccountItem]) -> list[Control]:
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
        for item in items:
            ui_items.append(item_row(item))
        return ui_items

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")

    def filter_items(self, type_list):
        if not isinstance(type_list, ItemTypesList):
            return
        
        items_of_types = []
        for t in type_list.selected_types:
            items_of_types.append(set(self.backend.current_items(key=BookItemSelectKeys.Type, type=t)))
        
        if len(items_of_types) <= 0:
            self.visible_items = self.backend.current_items()
        else:
            self.visible_items = set()
            for items in items_of_types:
                self.visible_items = self.visible_items | items
            self.visible_items = list(self.visible_items)
        
        self.visible_items_ui = self._parse_ui_items(self.visible_items)

        self.controls = self.visible_items_ui
        self.update()
        self.message_pub.invoke((self, type_list))


class ItemTypeButton(ft.FilledTonalButton):
    def __init__(self, type_id: int, text = None, icon = None, icon_color = None, color = None, bgcolor = None, content = None, elevation = None, style = None, autofocus = None, clip_behavior = None, url = None, url_target = None, on_click = None, on_long_press = None, on_hover = None, on_focus = None, on_blur = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(text, icon, icon_color, color, bgcolor, content, elevation, style, autofocus, clip_behavior, url, url_target, on_click, on_long_press, on_hover, on_focus, on_blur, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, adaptive)        
        self.text = f"{U.AccountItemTypes.CustomTypes[type_id].icon} {U.AccountItemTypes.CustomTypes[type_id].name}"
        self.expand = True
        self.style = ft.ButtonStyle(padding=10, text_style=ft.TextStyle(weight=ft.FontWeight.W_500), color=UIConfig.TypeButtonColor[0], bgcolor=UIConfig.TypeButtonColor[1])

        self.type_id = type_id
        self.selected = False

    def switch(self):
        self.selected = not self.selected
        if self.selected:
            self.color = UIConfig.TypeButtonColorSelected[0]
            self.bgcolor = UIConfig.TypeButtonColorSelected[1]
        else:
            self.color = UIConfig.TypeButtonColor[0]
            self.bgcolor = UIConfig.TypeButtonColor[1]
        self.update()
        return self.type_id


class ItemTypesList(ft.ListView):
    def __init__(self, backend: AccountingApp, controls = None, horizontal = None, spacing = None, item_extent = None, first_item_prototype = None, divider_thickness = None, padding = None, clip_behavior = None, semantic_child_count = None, cache_extent = None, build_controls_on_demand = None, auto_scroll = None, reverse = None, on_scroll_interval = None, on_scroll = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(controls, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding, clip_behavior, semantic_child_count, cache_extent, build_controls_on_demand, auto_scroll, reverse, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, adaptive)
        self.backend = backend

        self.message_pub = UIMessage()
        self.selected_types: list[U.AccountItemType] = []
        self._selected_type_ids = []

        self.controls = self.type_buttons()
        self.expand = True
        self.horizontal = True
        self.height = UIConfig.TypesListHeight
        self.spacing = UIConfig.TypesListSpacing

    def select_type(self, id: int):
        if id in self._selected_type_ids:
            return
        self._selected_type_ids.append(id)
        self.selected_types.append(U.AccountItemTypes.CustomTypes[id])

    def unselect_type(self, id: int):
        if id not in self._selected_type_ids:
            return
        self._selected_type_ids.remove(id)
        self.selected_types.remove(U.AccountItemTypes.CustomTypes[id])

    def type_button_click(self, e: ft.ControlEvent):
        button = e.control
        if isinstance(button, ItemTypeButton) and button.selected:
            self.unselect_type(button.type_id)
        elif isinstance(button, ItemTypeButton) and not button.selected:
            self.select_type(button.type_id)
        button.switch()
        self.message_pub.invoke(self)
        # U.print_list(self.selected_types)
    
    def type_buttons(self):
        buttons: list[ft.FilledTonalButton] = []
        for i in range(len(U.AccountItemTypes.CustomTypes)):
            buttons.append(ItemTypeButton(type_id=i, on_click=self.type_button_click))
        return buttons

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")


class CreateItemButton(ft.FloatingActionButton):
    def __init__(self, backend: AccountingApp, text = None, icon = None, bgcolor = None, content = None, shape = None, autofocus = None, mini = None, foreground_color = None, focus_color = None, clip_behavior = None, elevation = None, disabled_elevation = None, focus_elevation = None, highlight_elevation = None, hover_elevation = None, enable_feedback = None, url = None, url_target = None, mouse_cursor = None, on_click = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None):
        super().__init__(text, icon, bgcolor, content, shape, autofocus, mini, foreground_color, focus_color, clip_behavior, elevation, disabled_elevation, focus_elevation, highlight_elevation, hover_elevation, enable_feedback, url, url_target, mouse_cursor, on_click, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data)
        self.backend = backend

        self.icon = ft.Icons.ADD
        self.width = UIConfig.CreateItemButtonWidth
        self.height = UIConfig.CreateItemButtonHeight
        self.expand = False
        self.on_click = None  # TODO


class BottomRow(ft.Row):
    def __init__(self, backend: AccountingApp, controls = None, alignment = None, vertical_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(controls, alignment, vertical_alignment, spacing, tight, wrap, run_spacing, run_alignment, scroll, auto_scroll, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, adaptive)
        self.backend = backend

        self.width = UIConfig.BottomRowWidth
        self.height = UIConfig.BottomRowHeight

        self.item_types = ItemTypesList(self.backend)
        self.create_item_button = CreateItemButton(self.backend)
        self.controls = [self.item_types, self.create_item_button]
    
    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")


class MainColumn(ft.Column):
    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)
        self.backend = backend

        self.title_card = TitleCard(backend=self.backend)
        self.items_list = AccountItemList(backend=self.backend)
        self.bottom_bar = BottomRow(backend=self.backend)
        self.controls = [self.title_card, self.items_list, self.bottom_bar]

        self.expand=True
        self.spacing=UIConfig.ItemListSpacing
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")


class AccountingAppUI(ft.Container):
    """记账软件的前端 UI 部分"""
    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)
        self.backend = backend

        self.main_column = MainColumn(self.backend)

        # message subscriptions
        self.main_column.bottom_bar.item_types.message_pub.add(self.main_column.items_list.filter_items)
        self.main_column.items_list.message_pub.add(self.main_column.title_card.filtered_monthly_inout)
        
        self.content = self.main_column
        self.expand = True

    def update(self):
        super().update()
        self.content.update()
        print(f"{self.__class__.__name__} updated")