import datetime as dt
from datetime import datetime
import utils as U


class AccountItem:
    def __init__(self, type: U.AccountItemType | str, name: str, amount: float, time: datetime = None):
        self.__type = None
        self.type = type
        self.name = name
        self.datetime = datetime.now() if time is None else time
        self.amount = amount

    def __str__(self):
        return f"{self.type.name} {self.name} {self.datetime} {self.amount}"
    
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        if isinstance(value, U.AccountItemType):
            self.__type = value
        elif isinstance(value, str):
            for t in U.AccountItemTypes.CustomTypes:
                if t == value:
                    self.__type = t
                    break
        else:
            raise ValueError(f"Given value {value} ({type(value).__name__}) is not a valid type value")


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
    
    def create_item(self, type: U.AccountItemType | str, name: str, amount: float, time: datetime = None, **kwargs):
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
        """
        Usage:
        ```
        sort_items(key=BookItemSortKeys.Time)
        ```
        """
        self.items = sorted(self.items, key=key, reverse=descending)

    def select_items(self, key, sort_key = None, sort_descending: bool = True, **kwargs) -> list[AccountItem]:
        """
        Usage:
        ```
        sort_items(key=BookItemSelectKeys.AmountRange, sort_key=BookItemSortKeys.Amount, start=114, end=514)
        sort_items(key=BookItemSelectKeys.Type, type="Books")
        ```
        """
        selected = []
        for item in self.items:
            if key(item, **kwargs):
                selected.append(item)
        
        if sort_key is not None:
            selected = sorted(selected, key=sort_key, reverse=sort_descending)
        return selected


class BookItemSortKeys:
    @staticmethod
    def Time(item: AccountItem):
        return item.datetime
    
    @staticmethod
    def Amount(item: AccountItem):
        return item.amount
    

class BookItemSelectKeys:
    def Type(item: AccountItem, **kwargs):
        """
        是否为某个类型的账目\n
        kwargs:\n
        - `type: str | AccountItemType` (类型名 | 类型)
        """
        type = None
        if "type" in kwargs:
            type = kwargs["type"]

        if type is None:
            return True
        return item.type == type
    
    def TimeRange(item: AccountItem, **kwargs):
        """
        是否为某段时间内的账目\n
        kwargs:\n
        - `start: datetime`
        - `end: datetime`
        """
        from_time, to_time = None, None
        if "start" in kwargs:
            from_time = kwargs["start"]
        if "end" in kwargs:
            to_time = kwargs["end"]

        if from_time is not None and item.datetime < from_time:
            return False
        if to_time is not None and item.datetime > to_time:
            return False
        return True
    
    def AmountRange(item: AccountItem, **kwargs):
        """
        是否为某个花费范围内的账目\n
        kwargs:\n
        - `start: float`
        - `end: float`
        """
        from_amount, to_amount = None, None
        if "start" in kwargs:
            from_amount = kwargs["start"]
        if "end" in kwargs:
            to_amount = kwargs["end"]

        if from_amount is not None and item.amount < from_amount:
            return False
        if to_amount is not None and item.amount > to_amount:
            return False
        return True


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

    # test: book management
    print("----------")
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

    # test: crate and edit item
    print("----------")
    b2.create_item("Books", "haha", 114)
    b2.create_item(U.AccountItemTypes.Clothes, "lol", 514)
    U.print_list(b2.items)
    b2.edit_item(target_id=0, to_type="Games", to_time=U.random_datetime())
    U.print_list(b2.items)

    # test: select items
    print("----------")
    import random
    for _ in range(50):
        b1.create_item(
            type=random.choice(U.AccountItemTypes.CustomTypes),
            name="",
            amount=random.randrange(10, 200),
            time=U.random_datetime(year=False),
        )
    U.print_list(b1.items)
    print("\n", "select type books no sort")
    U.print_list(b1.select_items(key=BookItemSelectKeys.Type, type="Books"))
    print("\n", "select type clothes")
    U.print_list(b1.select_items(key=BookItemSelectKeys.Type, sort_key=BookItemSortKeys.Time, type="Clothes"))
    print("\n", "select amount from 11 to 45")
    U.print_list(b1.select_items(key=BookItemSelectKeys.AmountRange, sort_key=BookItemSortKeys.Amount, start=11, end=45))
    print("\n", "select datetime from 2025 feb to apr")
    U.print_list(b1.select_items(key=BookItemSelectKeys.TimeRange, sort_key=BookItemSortKeys.Time, start=datetime(2025, 1, 1), end=datetime(2025, 4, 1)))