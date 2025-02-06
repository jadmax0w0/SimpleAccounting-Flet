import flet as ft
from flet import Control
from data import *
from utils import *
from uiparts.config import UIConfig
from uiparts.messaging import UIMessage

from uiparts.typeslist import ItemTypesList


class AccountItemRow(ft.ListTile):
    def __init__(self, backend: AccountingApp, item: AccountItem):

        super().__init__()
        self.backend = backend
        self.item = item

        self.event_clicked = UIMessage()

        self.type_icon = AccountItemRow._item_text(value=item.type.icon, width=UIConfig.ItemIconWidth)
        self.title = AccountItemRow._item_text(value=item.name, weight=ft.FontWeight.BOLD, expand=True)
        self.time = AccountItemRow._item_text(value=item.datetime_info(), width=UIConfig.ItemTimeWidth)
        self.amount = AccountItemRow._item_text(
            value=item.amount_info, width=UIConfig.ItemAmountWidth, align=ft.TextAlign.RIGHT, 
            color=(ft.Colors.GREEN if item.amount >= 0 else ft.Colors.RED),
            weight=ft.FontWeight.BOLD,
        )
        self.content_row = ft.Row(controls=[self.type_icon, self.title, self.time, self.amount], vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

        self.title = self.content_row
        self.expand = True
        self.on_click = self.clicked

    @staticmethod
    def _item_text(value: str, weight: ft.FontWeight = UIConfig.ItemTextWeight, width: int = None, expand: bool = None, align = ft.TextAlign.CENTER, color: ft.Colors = None):
        return ft.Text(
            value=value,
            width=width,
            size=UIConfig.ItemTextSize,
            weight=weight,
            text_align=align,
            overflow=ft.TextOverflow.FADE,
            color=color,
            expand=expand,
        )

    def clicked(self, e):
        self.event_clicked.invoke(self.item)

    def update(self):
        super().update()
        for c in self.content_row.controls:
            c.update()


class AccountItemExpansionPanel(ft.ExpansionPanel):
    def __init__(self, backend: AccountingApp, items: list[AccountItem]):
        super().__init__()
        self.backend = backend
        self.items = items
        self.year_month = (self.items[0].datetime.year, self.items[0].datetime.month)

        self.event_item_clicked = UIMessage()

        self.year_month_text = ft.Text(
            value=self.items[0].datetime.strftime("%Y 年 %m 月"), 
            text_align=ft.TextAlign.LEFT, weight=UIConfig.ItemYearMonthTextWeight, size=UIConfig.ItemYearMonthTextSize, expand=True
        )
        self.monthly_inout = ft.Text(
            value=self.backend.addup(key=BookItemSelectKeys.SpecificMonth, items_list=self.items, year=self.year_month[0], month=self.year_month[1], to_info=True), 
            text_align=ft.TextAlign.RIGHT, weight=UIConfig.ItemYearMonthTextWeight, size=UIConfig.ItemYearMonthTextSize, expand=True
        )
        self.header_container = ft.Container(
            content=ft.Row([self.year_month_text, self.monthly_inout], expand=True),
            expand=True, padding=UIConfig.ItemYearMonthPadding
        )
        self.item_controls = self._parse_ui_items(self.items)
        self.item_column = ft.Column(controls=self.item_controls, expand=True)

        self.header = self.header_container
        self.content = self.item_column

    def _parse_ui_items(self, items: list[AccountItem]) -> list[Control]:
        ui_items = []
        for item in items:
            ui_item = AccountItemRow(self.backend, item)
            ui_item.event_clicked.add(self.item_clicked)
            ui_items.append(ui_item)
        return ui_items
    
    def item_clicked(self, item: AccountItem):
        self.event_item_clicked.invoke(item)

    def update(self):
        super().update()
        self.year_month_text.update()
        self.monthly_inout.update()
        for c in self.item_controls:
            c.update()

    def update_items(self, items: list[AccountItem]):
        self.items = items

        self.year_month = (self.items[0].datetime.year, self.items[0].datetime.month)
        self.year_month_text.value = self.items[0].datetime.strftime("%Y 年 %m 月")
        self.monthly_inout.value = self.backend.addup(key=BookItemSelectKeys.SpecificMonth, items_list=self.items, year=self.year_month[0], month=self.year_month[1], to_info=True)
        self.item_controls = self._parse_ui_items(self.items)
        self.item_column.controls = self.item_controls
        self.update()


class AccountItemList(ft.ListView):
    def __init__(self, backend: AccountingApp):
        super().__init__()
        self.backend = backend
        
        self.event_items_filtered = UIMessage()
        self.event_item_clicked = UIMessage()

        self.selected_year_month = {(datetime.now().year, datetime.now().month)}
        self.selected_types_cache: list[AccountItemType] = []
        self.visible_items: list[Control] = backend.current_items(sort_key=BookItemSortKeys.Time)
        self.visible_items_ui = self._parse_ui_items(self.visible_items)

        self.expansion_list_view = ft.ExpansionPanelList(
            controls=self.visible_items_ui, 
            spacing=UIConfig.ItemListSpacing, expand=True, on_change=self._expansion_panel_list_changed
        )

        self.controls = [self.expansion_list_view]  # 单独使用 expansion panel list 无法滚动，所以使用 listview 包裹
        self.padding = UIConfig.ItemListPadding
        self.spacing = UIConfig.ItemListSpacing
        self.expand = True
        self.width = UIConfig.ItemListWidth

    def _parse_ui_items(self, items: list[AccountItem]) -> list[Control]:
        ui_items = []

        year_months = self.backend.year_months(items)
        year_months = sorted(year_months, reverse=True)
        for year_month in year_months:
            items_of_year_month = self.backend.select_items(key=BookItemSelectKeys.SpecificMonth, items_list=items, year=year_month[0], month=year_month[1])
            ui_item = AccountItemExpansionPanel(self.backend, items_of_year_month)
            if year_month in self.selected_year_month:
                ui_item.expanded = True
            ui_item.event_item_clicked.add(self.item_clicked)
            
            ui_items.append(ui_item)

        return ui_items
    
    def _expansion_panel_list_changed(self, e):
        clicked_panel = self.expansion_list_view.controls[int(e.data)]
        if isinstance(clicked_panel, AccountItemExpansionPanel):
            if clicked_panel.expanded:
                self.selected_year_month.add((clicked_panel.year_month[0], clicked_panel.year_month[1]))
            else:
                self.selected_year_month.remove((clicked_panel.year_month[0], clicked_panel.year_month[1]))
        if len(self.selected_year_month) <= 0:
            self.selected_year_month.add((datetime.now().year, datetime.now().month))

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        for c in self.visible_items_ui:
            c.update()
        print(f"{self.__class__.__name__} updated")

    def filter_items(self, type_list: ItemTypesList):
        if isinstance(type_list, ItemTypesList):
            self.selected_types_cache = type_list.selected_types
        
        items_of_types = []
        for t in self.selected_types_cache:
            items_of_types.append(self.backend.current_items(key=BookItemSelectKeys.Type, type=t))
        
        if len(items_of_types) <= 0:
            self.visible_items = self.backend.current_items(sort_key=BookItemSortKeys.Time)
        else:
            self.visible_items = self.backend.merge_selected_items(False, *items_of_types)
            self.visible_items = self.backend.sort_items(key=BookItemSortKeys.Time, items_list=self.visible_items)
        
        self.visible_items_ui = self._parse_ui_items(self.visible_items)

        self.expansion_list_view.controls = self.visible_items_ui  # 更新 expansion list view 的 controls 而非 listview 的 controls
        self.update()
        self.event_items_filtered.invoke((self, type_list))
    
    def item_clicked(self, item: AccountItem):
        self.event_item_clicked.invoke(item)


class EmptyItemsHint(ft.Container):
    def __init__(self, backend: AccountingApp, content = None, padding = None, margin = None, alignment = None, bgcolor = None, gradient = None, blend_mode = None, border = None, border_radius = None, image_src = None, image_src_base64 = None, image_repeat = None, image_fit = None, image_opacity = None, shape = None, clip_behavior = None, ink = None, image = None, ink_color = None, animate = None, blur = None, shadow = None, url = None, url_target = None, theme = None, theme_mode = None, color_filter = None, ignore_interactions = None, foreground_decoration = None, on_click = None, on_tap_down = None, on_long_press = None, on_hover = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(content, padding, margin, alignment, bgcolor, gradient, blend_mode, border, border_radius, image_src, image_src_base64, image_repeat, image_fit, image_opacity, shape, clip_behavior, ink, image, ink_color, animate, blur, shadow, url, url_target, theme, theme_mode, color_filter, ignore_interactions, foreground_decoration, on_click, on_tap_down, on_long_press, on_hover, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, rtl, adaptive)
        self.backend = backend
        self.event_create_clicked = UIMessage()

        self.create_item_button = ft.IconButton(icon=ft.Icons.ADD, on_click=self.create_button_clicked)
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

    def create_button_clicked(self, e):
        self.event_create_clicked.invoke(None)