import flet as ft
import fire
from flet import Page, Control
import datetime as dt
from datetime import datetime
import constants as C


class Book:
    def __init__(self, name: str = "新账本", time: datetime = None):
        self.name = name
        self.create_time = datetime.now() if time is None else time
        self.items: list[AccountItem] = []

    def __str__(self):
        return f"Book \"{self.name}\" ({self.create_time}) with {len(self.items)} items"

    def addup(self) -> float:
        result = 0
        for item in self.items:
            result += item.amount
        return result


class BookStats:
    def __init__(self, activated: bool = True):
        self.activated = activated


class AccountItem:
    def __init__(self, type: C.AccountItemType, name: str, amount: float, time: datetime= None):
        self.type = type
        self.name = name
        self.datetime = datetime.now() if time is None else time
        self.amount = amount


class AccountingApp(Control):
    def __init__(self, ref = None, expand = None, expand_loose = None, col = None, opacity = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None):
        super().__init__(ref, expand, expand_loose, col, opacity, tooltip, badge, visible, disabled, data, rtl)
        
        self.books: list[tuple[Book, BookStats]] = []
        self.book_id = -1

    @property
    def current_book(self):
        if self.book_id >= 0 and self.book_id < len(self.books):
            book, stats = self.books[self.book_id]
            assert stats.activated is True, f"Book with id {self.book_id} is not activated"
            return book
    
    @current_book.setter
    def current_book(self, value: Book):
        for i in range(len(self.books)):
            b, _ = self.books[i]
            if b.name == value.name:
                self.book_id = i
                return
        self.books.append((value, BookStats()))
        self.book_id = len(self.books) - 1
        print(f"Warning: no book named \"{value.name}\" is found, created a new instead")

    def create_book(self, name: str = None, time: datetime = None, **kwargs):
        book = None
        if "book" in kwargs:
            book = kwargs["book"]
        book = Book(name, time) if book is None else book
        
        for b, _ in self.books:
            assert b.name != book.name, f"Book with name \"{book.name}\" already exists"
        self.books.append((book, BookStats()))

    def switch_book(self, id: int):
        assert id >= 0 and id < len(self.books)
        self.book_id = id

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


if __name__ == "__main__":
    b1, b2 = Book("a"), Book("b")
    b3 = Book("c")
    b4 = Book("c")
    app = AccountingApp()

    app.create_book(book=b1)
    app.create_book(book=b2)
    app.switch_book(1)
    print(str(app.current_book), app.book_id)
    app.current_book = b1
    print(str(app.current_book), app.book_id)
    app.current_book = b3
    app.create_book(book=b4)