import datetime as dt
from datetime import datetime
import utils as U


class AccountItem:
    def __init__(self, type: U.AccountItemType, name: str, amount: float, time: datetime = None):
        self.type = type
        self.name = name
        self.datetime = datetime.now() if time is None else time
        self.amount = amount

    def __str__(self):
        return f"{self.type.name} {self.name} {self.datetime} {self.amount}"


class Book:
    def __init__(self, name: str = "新账本", time: datetime = None):
        self.name = name
        self.create_time = datetime.now() if time is None else time
        self.items: list[AccountItem] = []

    def __str__(self):
        return f"Book \"{self.name}\" ({self.create_time}) with {len(self.items)} items"

    @property
    def addup(self) -> float:
        result = 0
        for item in self.items:
            result += item.amount
        return result
    
    def create_item(self, type: U.AccountItemType, name: str, amount: float, time: datetime = None, **kwargs):
        item = None
        if "item" in kwargs:
            item = kwargs["item"]
        else:
            item = AccountItem(type, name, amount, time)
        assert item is not None

        self.items.append(item)

    def edit_item(self, target_id: int, to_type = None, to_name = None, to_amount = None, to_time = None, **kwargs):
        target_item = None
        if "target_item" in kwargs:
            target_item = kwargs["target_item"]
        else:
            assert target_id >= 0 and target_id <= len(self.items)
            target_item = self.items[target_id]
        assert target_item is not None

        if "like" in kwargs:
            to_item: AccountItem = kwargs["like"]
            to_type = to_item.type if to_item.type is not None else to_type
            to_name = to_item.name if to_item.name is not None else to_name
            to_amount = to_item.amount if to_item.amount is not None else to_amount
            to_time = to_item.datetime if to_item.datetime is not None else to_time

        if to_type is not None:
            target_item.type = to_type
        if to_name is not None:
            target_item.name = to_name
        if to_amount is not None:
            target_item.amount = to_amount
        if to_time is not None:
            target_item.datetime = to_time

    def delete_item(self, target_id: int, **kwargs):
        target_item = None
        if "target_item" in kwargs:
            target_item = kwargs["target_item"]
        else:
            assert target_id >= 0 and target_id < len(self.items)
            target_item = self.items[target_id]
        assert target_item is not None

        self.items.remove(target_item)

    def sort_items(self, key, descending: bool = True):
        self.items = sorted(self.items, key=key, reverse=descending)

    def select_items():
        # TODO
        pass


class BookItemSortKeys:
    @staticmethod
    def Time(item: AccountItem):
        return item.datetime
    
    @staticmethod
    def Amount(item: AccountItem):
        return item.amount

class BookStats:
    def __init__(self, activated: bool = True):
        self.activated = activated


class AccountingApp:
    """记账软件的后端数据部分"""

    def __init__(self):
        self.books: list[tuple[Book, BookStats]] = []
        self.book_id = -1

    @property
    def current_book(self):
        assert self.book_id >= 0 and self.book_id < len(self.books)
        book, stats = self.books[self.book_id]
        assert stats.activated is True, f"Book with id {self.book_id} is not activated"
        return book
    
    @current_book.setter
    def current_book(self, value: Book | str):
        for i in range(len(self.books)):
            b, _ = self.books[i]
            if (isinstance(value, Book) and (b == value or b.name == value.name)) or (isinstance(value, str) and value == b.name):
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
    print(len(app.books))
    app.current_book = b3  # add new book
    print(len(app.books))
    try:
        app.create_book(book=b4)
    except AssertionError as e:
        print(e)
    app.current_book = "a"
    print(str(app.current_book), app.book_id)

    b1.create_item(U.AccountItemTypes.Books, "book1", 14.5)