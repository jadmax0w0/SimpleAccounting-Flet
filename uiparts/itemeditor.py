import flet as ft
from data import *
from uiparts.messaging import UIMessage
from uiparts.typeslist import ItemTypesList


class ItemInfoEditor(ft.Column):

    def __init__(self, backend: AccountingApp, controls = None, alignment = None, horizontal_alignment = None, spacing = None, tight = None, wrap = None, run_spacing = None, run_alignment = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, visible = None, disabled = None, data = None, rtl = None, scroll = None, auto_scroll = None, on_scroll_interval = None, on_scroll = None, adaptive = None):
        super().__init__(controls, alignment, horizontal_alignment, spacing, tight, wrap, run_spacing, run_alignment, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, visible, disabled, data, rtl, scroll, auto_scroll, on_scroll_interval, on_scroll, adaptive)
        self.backend = backend
        self.item = None
        self.selected_date = datetime.now()

        self.event_delete = UIMessage()
        self.event_confirm = UIMessage()
        self.event_cancel = UIMessage()

        self.type_select = ft.Dropdown(options=self._parse_type_options(), label="账目类型")
        self.name_input = ft.TextField(label="记账内容")
        self.amount_input = ft.TextField(label="数额", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
        self.income_expense = ft.SegmentedButton(
            width=200,
            selected={"out"},
            segments=[
                ft.Segment(value="in", label=ft.Text("收入")),
                ft.Segment(value="out", label=ft.Text("支出")),
            ],
        )
        self.selected_date_text = ft.Text(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.date_button = ft.ElevatedButton(text="选择日期", on_click=self.pick_date, height=45)
        self.delete_button = ft.ElevatedButton(text="删除", width=100, height=50, bgcolor=ft.colors.RED, color=ft.colors.WHITE, on_click=self.on_delete)
        self.confirm_button = ft.ElevatedButton(text="确定", width=100, height=50, on_click=self.on_confirm)
        self.cancel_button = ft.ElevatedButton(text="取消", width=100, height=50, on_click=self.on_cancel)

        self.controls = [
            self.type_select,
            self.name_input,
            ft.Row([
                self.amount_input,
                self.income_expense
            ], alignment=ft.MainAxisAlignment.START),
            ft.Row([self.date_button, self.selected_date_text]),
            ft.Row(
                [
                    ft.Container(content=self.delete_button, alignment=ft.alignment.center_left),
                    ft.Container(
                        content=ft.Row(
                            [self.cancel_button, self.confirm_button],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        alignment=ft.alignment.center_right,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
        ]
        self.expand = True

    def _parse_type_options(self):
        options = []
        for t in U.AccountItemTypes.CustomTypes:
            title = f"{t.icon} {t.name}"
            options.append(ft.dropdown.Option(key=t.name, text=title))
        return options

    def update(self):
        super().update()
        self.type_select.update()
        self.name_input.update()
        self.amount_input.update()
        self.income_expense.update()
        self.selected_date_text.update()
        self.date_button.update()
        self.confirm_button.update()
        self.cancel_button.update()

    def on_pop_up(self, item: AccountItem):
        def set_item(item: AccountItem):
            self.item = item
            if item is not None:
                self.type_select.value = item.type.name
                self.name_input.value = item.name
                self.amount_input.value = str(abs(item.amount))
                self.income_expense.selected = {"in"} if item.amount > 0 else {"out"}
                self.selected_date = item.datetime
                self.selected_date_text.value = self.selected_date.strftime("%Y-%m-%d")
                self.delete_button.visible = True
            else:
                # self.type_select.value = None
                self.name_input.value = ""
                self.amount_input.value = ""
                self.income_expense.selected = {"out"}
                self.selected_date = datetime.now()
                self.selected_date_text.value = datetime.now().strftime("%Y-%m-%d")
                self.delete_button.visible = False

        set_item(item)
        self.update()

    def on_delete(self, sender):
        def confirm_delete(e):
            if e.control.data == "yes":
                self.event_delete.invoke(self.item)
            self.page.close(confirmation)

        confirmation = ft.AlertDialog(
            title=ft.Text("确认删除"),
            content=ft.Text("确定要删除这条账目吗？"),
            actions=[
                ft.TextButton("取消", data="no", on_click=confirm_delete),
                ft.TextButton("确定", data="yes", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(confirmation)

    def on_confirm(self, sender):
        # 首先检测信息是否填写完整

        if self.type_select.value is None or len(self.type_select.value) == 0:
            print("Warning: type not selected")
            return
        if len(self.name_input.value) == 0:
            print("Warning: name not filled")
            return
        try:
            amount = float(self.amount_input.value)
            if amount <= 0:
                raise ValueError
        except ValueError:
            print("Warning: invalid amount")
            return
        if "out" in self.income_expense.selected:
            amount = -amount
        
        # 然后调用事件
        self.event_confirm.invoke({
            "type": self.type_select.value,
            "name": self.name_input.value,
            "amount": amount,
            "date": self.selected_date,
            "item": self.item,
        })

    def on_cancel(self, sender):
        self.event_cancel.invoke(None)

    def set_filtered_type(self, sender: ItemTypesList):
        if len(sender.selected_types) <= 0:
            return
        type = sender.selected_types[-1]
        for option in self.type_select.options:
            if option.key == type.name:

                self.type_select.value = option.key
                break

    def pick_date(self, e):
        def date_picker_on_change(e):
            self.selected_date = e.control.value
            self.selected_date_text.value = self.selected_date.strftime("%Y-%m-%d %H:%M")
            self.update()
        
        date_picker = ft.DatePicker(
            on_change=date_picker_on_change,
            first_date=datetime(1900, 1, 1),
            last_date=datetime(2100, 12, 31),
            value=self.selected_date
        )
        self.page.open(date_picker)


class ItemInfoEditorContainer(ft.Container):
    def __init__(self, backend: AccountingApp, content = None, padding = None, margin = None, alignment = None, bgcolor = None, gradient = None, blend_mode = None, border = None, border_radius = None, image_src = None, image_src_base64 = None, image_repeat = None, image_fit = None, image_opacity = None, shape = None, clip_behavior = None, ink = None, image = None, ink_color = None, animate = None, blur = None, shadow = None, url = None, url_target = None, theme = None, theme_mode = None, color_filter = None, ignore_interactions = None, foreground_decoration = None, on_click = None, on_tap_down = None, on_long_press = None, on_hover = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(content, padding, margin, alignment, bgcolor, gradient, blend_mode, border, border_radius, image_src, image_src_base64, image_repeat, image_fit, image_opacity, shape, clip_behavior, ink, image, ink_color, animate, blur, shadow, url, url_target, theme, theme_mode, color_filter, ignore_interactions, foreground_decoration, on_click, on_tap_down, on_long_press, on_hover, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, rtl, adaptive)
        self.backend = backend

        self.item_editor = ItemInfoEditor(self.backend)
        self.content = self.item_editor
        self.expand = True
        self.padding = 15
        # TODO: 把那些按钮之类的也在这里写个属性，方便外面引用

    def update(self):
        super().update()
        self.content.update()


class ItemInfoEditorBottomSheet(ft.BottomSheet):
    def __init__(self, backend: AccountingApp, content = None, open = False, elevation = None, bgcolor = None, dismissible = None, enable_drag = None, show_drag_handle = None, use_safe_area = None, is_scroll_controlled = None, maintain_bottom_view_insets_padding = None, animation_style = None, size_constraints = None, clip_behavior = None, shape = None, on_dismiss = None, ref = None, disabled = None, visible = None, data = None):
        super().__init__(content, open, elevation, bgcolor, dismissible, enable_drag, show_drag_handle, use_safe_area, is_scroll_controlled, maintain_bottom_view_insets_padding, animation_style, size_constraints, clip_behavior, shape, on_dismiss, ref, disabled, visible, data)
        self.backend = backend

        self.editor_container = ItemInfoEditorContainer(self.backend)

        self.content = self.editor_container

    def update(self):
        super().update()
        self.content.update()
