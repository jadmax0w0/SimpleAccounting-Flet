import flet as ft
from flet import Page, Control
from data import *
import utils as U
from typing import Callable


class UIConfig:
    # title card
    BookTitleTextSize = 25
    BookTitleTextWeight = ft.FontWeight.W_600

    TitleYearTextSize = 20
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
    TitleCardHeight = 185
    TitleCardInnerPadding = ft.Padding(30, 15, 30, 15)
    
    # item list
    ItemTextSize = 15
    ItemTextWeight = ft.FontWeight.W_400
    ItemIconWidth = 20
    ItemNameWidth = 150
    ItemAmountWidth = 100

    ItemListPadding = ft.Padding(30, 0, 30, 0)
    ItemListSpacing = 15
    ItemListWidth = None

    EmptyItemsHintWidth = 300
    EmptyItemsHintPadding = ft.Padding(0, 0, 0, 80)  # BottomRowHeight

    # bottom bar
    TypesListHeight = 35
    TypesListSpacing = 15
    TypeButtonWidth = 65
    TypeButtonColor = ft.Colors.PRIMARY, ft.Colors.PRIMARY_CONTAINER
    TypeButtonColorSelected = ft.Colors.ON_PRIMARY, ft.Colors.ON_PRIMARY_CONTAINER
    CreateItemButtonWidth = 60
    CreateItemButtonHeight = 60
    BottomRowPadding = ft.Padding(10, 0, 10, 0)
    BottomRowWidth = None
    BottomRowHeight = 80
    BottomRowBlur = 10

    # main column
    MainPadding = 15


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


class AccountItemRow(ft.Row):
    def __init__(self, backend: AccountingApp, item: AccountItem, controls = None, alignment = None, vertical_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(controls, alignment, vertical_alignment, spacing, tight, wrap, run_spacing, run_alignment, scroll, auto_scroll, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, adaptive)
        self.backend = backend
        self.item = item

        self.type_icon = AccountItemRow._item_text(value=item.type.icon, width=UIConfig.ItemIconWidth)
        self.title = AccountItemRow._item_text(value=item.name, width=UIConfig.ItemNameWidth)
        self.time = AccountItemRow._item_text(value=item.datetime_info, expand=True)
        self.amount = AccountItemRow._item_text(
            value=item.amount_info, width=UIConfig.ItemAmountWidth, align=ft.TextAlign.RIGHT, 
            color=(ft.Colors.GREEN if item.amount >= 0 else ft.Colors.RED)
        )

        self.controls=[self.type_icon, self.title, self.time, self.amount]
        self.expand = True

    @staticmethod
    def _item_text(value: str, width: int = None, expand: bool = None, align = ft.TextAlign.CENTER, color: ft.Colors = None):
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


class AccountItemList(ft.ListView):
    def __init__(self, backend: AccountingApp, controls = None, horizontal = None, spacing = None, item_extent = None, first_item_prototype = None, divider_thickness = None, padding = None, clip_behavior = None, semantic_child_count = None, cache_extent = None, build_controls_on_demand = None, auto_scroll = None, reverse = None, on_scroll_interval = None, on_scroll = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(controls, horizontal, spacing, item_extent, first_item_prototype, divider_thickness, padding, clip_behavior, semantic_child_count, cache_extent, build_controls_on_demand, auto_scroll, reverse, on_scroll_interval, on_scroll, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, adaptive)
        self.backend = backend
        
        self.event_items_filtered = UIMessage()
        self.visible_items: list[Control] = backend.current_items(sort_key=BookItemSortKeys.Time)
        self.visible_items_ui = self._parse_ui_items(self.visible_items)
        self.controls = self.visible_items_ui

        self.padding = UIConfig.ItemListPadding
        self.spacing = UIConfig.ItemListSpacing
        self.expand = True
        self.width = UIConfig.ItemListWidth

    def _parse_ui_items(self, items: list[AccountItem]) -> list[Control]:
        ui_items = []
        for item in items:
            ui_items.append(AccountItemRow(self.backend, item))
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
            items_of_types.append(self.backend.current_items(key=BookItemSelectKeys.Type, type=t))
        
        if len(items_of_types) <= 0:
            self.visible_items = self.backend.current_items(sort_key=BookItemSortKeys.Time)
        else:
            self.visible_items = self.backend.merge_selected_items(False, *items_of_types)
            self.visible_items = self.backend.sort_items(key=BookItemSortKeys.Time, items_list=self.visible_items)
        
        self.visible_items_ui = self._parse_ui_items(self.visible_items)

        self.controls = self.visible_items_ui
        self.update()
        self.event_items_filtered.invoke((self, type_list))


class EmptyItemsHint(ft.Container):
    def __init__(self, backend: AccountingApp, content = None, padding = None, margin = None, alignment = None, bgcolor = None, gradient = None, blend_mode = None, border = None, border_radius = None, image_src = None, image_src_base64 = None, image_repeat = None, image_fit = None, image_opacity = None, shape = None, clip_behavior = None, ink = None, image = None, ink_color = None, animate = None, blur = None, shadow = None, url = None, url_target = None, theme = None, theme_mode = None, color_filter = None, ignore_interactions = None, foreground_decoration = None, on_click = None, on_tap_down = None, on_long_press = None, on_hover = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(content, padding, margin, alignment, bgcolor, gradient, blend_mode, border, border_radius, image_src, image_src_base64, image_repeat, image_fit, image_opacity, shape, clip_behavior, ink, image, ink_color, animate, blur, shadow, url, url_target, theme, theme_mode, color_filter, ignore_interactions, foreground_decoration, on_click, on_tap_down, on_long_press, on_hover, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, rtl, adaptive)
        self.backend = backend

        self.create_item_button = ft.IconButton(icon=ft.Icons.ADD)  # TODO: on click
        self.hint = ft.ListTile(
            title=ft.Text("无账目"),
            subtitle=ft.Text("开始记下第一笔账吧"),
            leading=ft.Icon(ft.Icons.SAVINGS),
            trailing=self.create_item_button,
            width=UIConfig.EmptyItemsHintWidth,
        )

        self.content = self.hint
        self.padding = UIConfig.EmptyItemsHintPadding
        self.alignment = ft.alignment.center
        self.expand = True


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

        self.event_type_button_click = UIMessage()
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
        self.event_type_button_click.invoke(self)
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


class BottomRowContainer(ft.Container):
    def __init__(self, backend: AccountingApp, content = None, padding = None, margin = None, alignment = None, bgcolor = None, gradient = None, blend_mode = None, border = None, border_radius = None, image_src = None, image_src_base64 = None, image_repeat = None, image_fit = None, image_opacity = None, shape = None, clip_behavior = None, ink = None, image = None, ink_color = None, animate = None, blur = None, shadow = None, url = None, url_target = None, theme = None, theme_mode = None, color_filter = None, ignore_interactions = None, foreground_decoration = None, on_click = None, on_tap_down = None, on_long_press = None, on_hover = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(content, padding, margin, alignment, bgcolor, gradient, blend_mode, border, border_radius, image_src, image_src_base64, image_repeat, image_fit, image_opacity, shape, clip_behavior, ink, image, ink_color, animate, blur, shadow, url, url_target, theme, theme_mode, color_filter, ignore_interactions, foreground_decoration, on_click, on_tap_down, on_long_press, on_hover, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, rtl, adaptive)
        self.backend = backend

        self.item_types = ItemTypesList(self.backend)
        self.create_item_button = CreateItemButton(self.backend)
        self.row = ft.Row(controls=[self.item_types, self.create_item_button], width=UIConfig.BottomRowWidth, height=UIConfig.BottomRowHeight)

        self.content = self.row
        self.width = UIConfig.BottomRowWidth
        self.height = UIConfig.BottomRowHeight
        self.blur = UIConfig.BottomRowBlur
        self.padding = UIConfig.BottomRowPadding
        self.expand = True
    
    def update(self):
        super().update()
        self.item_types.update()
        self.create_item_button.update()
        self.row.update()
        print(f"{self.__class__.__name__} updated")


class BottomContainer(ft.Container):
    def __init__(self, backend: AccountingApp, content = None, padding = None, margin = None, alignment = None, bgcolor = None, gradient = None, blend_mode = None, border = None, border_radius = None, image_src = None, image_src_base64 = None, image_repeat = None, image_fit = None, image_opacity = None, shape = None, clip_behavior = None, ink = None, image = None, ink_color = None, animate = None, blur = None, shadow = None, url = None, url_target = None, theme = None, theme_mode = None, color_filter = None, ignore_interactions = None, foreground_decoration = None, on_click = None, on_tap_down = None, on_long_press = None, on_hover = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(content, padding, margin, alignment, bgcolor, gradient, blend_mode, border, border_radius, image_src, image_src_base64, image_repeat, image_fit, image_opacity, shape, clip_behavior, ink, image, ink_color, animate, blur, shadow, url, url_target, theme, theme_mode, color_filter, ignore_interactions, foreground_decoration, on_click, on_tap_down, on_long_press, on_hover, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, rtl, adaptive)
        self.backend = backend

        self.row_content = BottomRowContainer(self.backend)
        self.content = self.row_content
        self.expand = True


class MainColumn(ft.Column):
    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)
        self.backend = backend

        self.title_card = TitleCard(backend=self.backend)
        self.items_list = AccountItemList(backend=self.backend)
        self.empty_items_hint = EmptyItemsHint(backend=self.backend)
        self.controls = [self.title_card, self.empty_items_hint]

        self.expand=True
        self.spacing=UIConfig.ItemListSpacing
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")

    def items_updated(self):
        if self.backend.current_items() is not None and len(self.backend.current_items()) > 0:
            self.controls = [self.title_card, self.items_list]
        else:
            self.controls = [self.title_card, self.empty_items_hint]
        self.update()


class MainStack(ft.Stack):
    def __init__(self, backend: AccountingApp, controls = None, clip_behavior = None, alignment = None, fit = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(controls, clip_behavior, alignment, fit, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, adaptive)
        self.backend = backend

        self.main_column = MainColumn(self.backend)
        self.bottom_bar = BottomContainer(self.backend)
        self.controls = [self.main_column, self.bottom_bar]
        self.expand = True
        self.alignment = ft.alignment.bottom_center

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

        # self.main_column = MainColumn(self.backend)
        self.main_stack = MainStack(self.backend)

        # message subscriptions
        self.main_stack.bottom_bar.row_content.item_types.event_type_button_click.add(self.main_stack.main_column.items_list.filter_items)
        self.main_stack.main_column.items_list.event_items_filtered.add(
            self.main_stack.main_column.title_card.filtered_monthly_inout,
            self.main_stack.main_column.items_updated,
        )
        
        self.content = self.main_stack
        self.expand = True

    def update(self):
        super().update()
        self.content.update()
        print(f"{self.__class__.__name__} updated")