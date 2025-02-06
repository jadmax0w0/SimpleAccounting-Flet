import flet as ft
from data import *

from uiparts.config import UIConfig
from uiparts.title import TitleCard
from uiparts.itemlist import AccountItemList, EmptyItemsHint
from uiparts.bottom import BottomContainer
from uiparts.itemeditor import ItemInfoEditorBottomSheet


class MainColumn(ft.Column):

    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)
        self.backend = backend

        self.title_card = TitleCard(backend=self.backend)
        self.items_list = AccountItemList(backend=self.backend)
        self.empty_items_hint = EmptyItemsHint(backend=self.backend)
        self.controls = [self.title_card, self.items_list, self.empty_items_hint]

        if self.items_list.visible_items is not None and len(self.items_list.visible_items) > 0:
            self.items_list.visible = True
            self.empty_items_hint.visible = False
        else:
            self.items_list.visible = False
            self.empty_items_hint.visible = True

        self.expand=True
        self.spacing=UIConfig.ItemListSpacing
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER

    def update(self):
        super().update()
        for c in self.controls:
            c.update()
        print(f"{self.__class__.__name__} updated")

    def items_updated(self, sender):
        if self.items_list.visible_items is not None and len(self.items_list.visible_items) > 0:
            self.items_list.visible = True
            self.empty_items_hint.visible = False
        else:
            self.items_list.visible = False
            self.empty_items_hint.visible = True
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

        # main content
        self.main_stack = MainStack(self.backend)

        # pop-up
        self.item_info_editor = ItemInfoEditorBottomSheet(self.backend)

        # message subscriptions
        # 点击界面底部的类别按钮时
        self.main_stack.bottom_bar.row_content.item_types.event_type_button_click.add(
            self.main_stack.main_column.items_list.filter_items,
            self.item_info_editor.editor_container.item_editor.set_filtered_type,
        )
        # 点击类别按钮后筛选好对应类别的账目时
        self.main_stack.main_column.items_list.event_items_filtered.add(
            self.main_stack.main_column.title_card.filtered_monthly_inout,
            self.main_stack.main_column.items_updated,
        )
        # 点击新增账目/编辑账目按钮或账目时
        self.main_stack.main_column.empty_items_hint.event_create_clicked.add(self.open_item_info_editor)
        self.main_stack.bottom_bar.row_content.create_item_button.event_clicked.add(self.open_item_info_editor)
        self.main_stack.main_column.items_list.event_item_clicked.add(self.open_item_info_editor)
        # 点击账目编辑页面中的确认/取消按钮时
        self.item_info_editor.editor_container.item_editor.event_confirm.add(self.append_or_edit_item)
        self.item_info_editor.editor_container.item_editor.event_cancel.add(self.close_item_info_editor)

        self.content = self.main_stack
        self.expand = True

    def update(self):
        super().update()
        self.content.update()
        print(f"{self.__class__.__name__} updated")

    def open_item_info_editor(self, item: AccountItem):
        self.page.open(self.item_info_editor)
        self.item_info_editor.editor_container.item_editor.on_pop_up(item)

    def close_item_info_editor(self, sender):
        self.page.close(self.item_info_editor)
    
    def append_or_edit_item(self, sender):
        if sender["item"] is None:
            self.backend.append_item(sender["type"], sender["name"], sender["amount"], sender["date"])
        else:
            self.backend.edit_item(sender["item"], sender["type"], sender["name"], sender["amount"], sender["date"])
        self.close_item_info_editor(sender)

        print(f"New item appended/edited: {sender}")
        self.update()