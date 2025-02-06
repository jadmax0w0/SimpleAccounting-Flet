import flet as ft
from data import *
from uiparts.config import UIConfig
from uiparts.messaging import UIMessage


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
        self.event_clicked = UIMessage()

        self.icon = ft.Icons.ADD
        self.width = UIConfig.CreateItemButtonWidth
        self.height = UIConfig.CreateItemButtonHeight
        self.expand = False
        self.on_click = self.clicked

    def clicked(self, e):
        self.event_clicked.invoke(None)