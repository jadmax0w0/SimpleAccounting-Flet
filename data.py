import datetime as dt
from datetime import datetime, timedelta
import utils as U
from typing import Callable
import json


class AccountItem:
    def __init__(self, type: U.AccountItemType | str, name: str, amount: float, time: datetime = None):
        self.__type = None
        self.type = type
        self.name = name
        self.datetime = datetime.now() if time is None else time
        self.amount = amount

    def __str__(self):
        return f"AccountItem: ({self.type}, {self.name}, {self.datetime}, {self.amount})"
    
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
        
    def datetime_info(self, verbose: bool = False):
        if verbose:
            return f"{self.datetime.year} 年 {self.datetime.month} 月 {self.datetime.day} 日 {self.datetime.hour:02}:{self.datetime.minute:02}"
        else:
            return f"{self.datetime.year} 年 {self.datetime.month} 月 {self.datetime.day} 日"
    
    @property
    def amount_info(self):
        return ("+" if self.amount > 0 else "") + f"{self.amount:.2f}"
    

class AccountItemJson(json.JSONEncoder):
    def __init__(self, *, skipkeys = False, ensure_ascii = True, check_circular = True, allow_nan = True, sort_keys = False, indent = None, separators = None, default = None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators, default=default)

    def default(self, o):
        if not isinstance(o, AccountItem):
            return super().default(o)
        return AccountItemJson.encode_dict(o)

    @staticmethod
    def encode_dict(o: AccountItem):
        return {
            "type": o.type.name,
            "name": o.name,
            "amount": o.amount,
            "datetime": (o.datetime.year, o.datetime.month, o.datetime.day, o.datetime.hour, o.datetime.minute, o.datetime.second, o.datetime.microsecond),
        }
    
    @staticmethod
    def decode(d):
        dtinfo = d["datetime"]
        return AccountItem(
            type=d["type"],
            name=d["name"],
            amount=d["amount"],
            time=datetime(dtinfo[0], dtinfo[1], dtinfo[2], dtinfo[3], dtinfo[4], dtinfo[5], dtinfo[6]),
        )


class Book:
    def __init__(self, name: str = "新账本", time: datetime = None):
        self.name = name
        self.create_time = datetime.now() if time is None else time
        self.items: list[AccountItem] = []

    def __str__(self):
        return f"Book: ({self.name}, {self.create_time}, {len(self.items)} items)"

    def addup(self, key: Callable[..., bool] = None, **kwargs) -> float:
        items = self.items
        if key is not None:
            items = self.select_items(key, **kwargs)

        result = 0
        for item in items:
            result += item.amount
        return result
    
    def create_item(self, type: U.AccountItemType | str = None, name: str = None, amount: float = None, time: datetime = None, **kwargs):
        item = None
        if "item" in kwargs:
            item = kwargs["item"]
        else:
            item = AccountItem(type, name, amount, time)
        assert item is not None

        self.items.append(item)

    def edit_item(self, item: AccountItem, to_type = None, to_name = None, to_amount = None, to_time = None, **kwargs):
        if not isinstance(item, AccountItem) or item not in self.items:
            return
        if item not in self.items:
            print(f"Warning: editing an item ({item}) not existing in {self}")
        
        if "like" in kwargs:
            to_item: AccountItem = kwargs["like"]
            to_type = to_item.type if to_item.type is not None else to_type
            to_name = to_item.name if to_item.name is not None else to_name
            to_amount = to_item.amount if to_item.amount is not None else to_amount
            to_time = to_item.datetime if to_item.datetime is not None else to_time

        if to_type is not None:
            item.type = to_type
        if to_name is not None:
            item.name = to_name
        if to_amount is not None:
            item.amount = to_amount
        if to_time is not None:
            item.datetime = to_time

    def delete_item(self, item: AccountItem):
        if not isinstance(item, AccountItem) or item not in self.items:
            return
        if item not in self.items:
            print(f"Warning: attempting to delete an item ({item}) not existing in {self}; omit")
            return

        self.items.remove(item)

    def sort_items(self, key: Callable = None, descending: bool = True):
        """
        Usage:
        ```
        sort_items(key=BookItemSortKeys.Time)
        ```
        """
        if key is not None:
            self.items = sorted(self.items, key=key, reverse=descending)

    def select_items(self, key: Callable[..., bool] = None, sort_key: Callable = None, sort_descending: bool = True, **kwargs) -> list[AccountItem]:
        """
        Usage:
        ```
        sort_items(key=BookItemSelectKeys.AmountRange, sort_key=BookItemSortKeys.Amount, start=114, end=514)
        sort_items(key=BookItemSelectKeys.Type, type="Books")
        ```
        """
        selected = [] if key is not None else self.items
        if len(selected) <= 0:
            for item in self.items:
                if key(item, **kwargs):
                    selected.append(item)
        
        if sort_key is not None:
            selected = sorted(selected, key=sort_key, reverse=sort_descending)
        return selected


class BookJson(json.JSONEncoder):
    def __init__(self, *, skipkeys = False, ensure_ascii = True, check_circular = True, allow_nan = True, sort_keys = False, indent = None, separators = None, default = None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators, default=default)

    def default(self, o):
        if isinstance(o, Book):
            return BookJson.encode_dict(o)
        return super().default(o)

    @staticmethod
    def encode_dict(o: Book):
        items_serialized = []
        for item in o.items:
            item = AccountItemJson.encode_dict(item)
            items_serialized.append(item)
        return {
            "name": o.name,
            "create_time": (o.create_time.year, o.create_time.month, o.create_time.day, o.create_time.hour, o.create_time.minute, o.create_time.second, o.create_time.microsecond),
            "items": items_serialized,
        }
    
    @staticmethod
    def decode(d):
        dtinfo = d["create_time"]
        b = Book(name=d["name"], time=datetime(dtinfo[0], dtinfo[1], dtinfo[2], dtinfo[3], dtinfo[4], dtinfo[5], dtinfo[6]))
        for dd in d["items"]:
            item = AccountItemJson.decode(dd)
            b.create_item(item=item)
        return b


class BookItemSortKeys:
    @staticmethod
    def Time(item: AccountItem):
        return item.datetime
    
    @staticmethod
    def Amount(item: AccountItem):
        return item.amount
    

class BookItemSelectKeys:
    @staticmethod
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
    
    @staticmethod
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
        
        include_start, include_end = True, True
        if "include_start" in kwargs:
            include_start = kwargs["include_start"]
        if "include_end" in kwargs:
            include_end = kwargs["include_end"]

        before_start = from_time is not None and ((item.datetime < from_time) if include_start else (item.datetime <= from_time))
        after_end = to_time is not None and ((item.datetime > to_time) if include_end else (item.datetime >= to_time))

        if before_start:
            return False
        if after_end:
            return False
        return True
    
    @staticmethod
    def SpecificYear(item: AccountItem, **kwargs):
        """
        是否为某年内的账目\n
        kwargs:\n
        - `year: int | None`
        """
        year = datetime.now().year
        if "year" in kwargs:
            year = kwargs["year"] if kwargs["year"] is not None else year
        
        return BookItemSelectKeys.TimeRange(item, start=datetime(year, 1, 1), end=datetime(year + 1, 1, 1), include_end=False)
    
    @staticmethod
    def SpecificMonth(item: AccountItem, **kwargs):
        """
        是否为某月内的账目\n
        kwargs:\n
        - `year: int | None`
        - `month: int | None`
        """
        year1 = datetime.now().year
        month1 = datetime.now().month
        if "year" in kwargs:
            year1 = kwargs["year"] if kwargs["year"] is not None else year1
        if "month" in kwargs:
            month1 = kwargs["month"] if kwargs["month"] is not None else month1

        year2 = year1
        month2 = month1 + 1
        if month2 >= 13:
            year2 = year1 + 1
            month2 = 1

        return BookItemSelectKeys.TimeRange(item, start=datetime(year1, month1, 1), end=datetime(year2, month2, 1), include_end=False)
    
    @staticmethod
    def SpecificDay(item: AccountItem, **kwargs):
        """
        是否为某天内的账目\n
        kwargs:\n
        - `year: int | None`
        - `month: int | None`
        - `day: int | None`
        """
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        if "year" in kwargs:
            year = kwargs["year"] if kwargs["year"] is not None else year
        if "month" in kwargs:
            month = kwargs["month"] if kwargs["month"] is not None else month
        if "day" in kwargs:
            day = kwargs["day"] if kwargs["day"] is not None else day
        
        start_time = datetime(year, month, day)
        end_time = start_time + timedelta(days=1)

        return BookItemSelectKeys.TimeRange(item, start=start_time, end=end_time, include_end=False)
    
    @staticmethod
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

    def __str__(self):
        return f"BookStats: {str(self.__dict__)}"


class BookStatsJson(json.JSONEncoder):
    def __init__(self, *, skipkeys = False, ensure_ascii = True, check_circular = True, allow_nan = True, sort_keys = False, indent = None, separators = None, default = None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators, default=default)

    def default(self, o):
        if isinstance(o, BookStats):
            return BookStatsJson.encode_dict(o)
        return super().default(o)

    @staticmethod
    def encode_dict(o: BookStats):
        return o.__dict__

    @staticmethod
    def decode(d):
        return BookStats(d["activated"])


class AccountingApp:
    """记账软件的后端数据部分"""

    def __init__(self, books: list[tuple[Book, BookStats]] = [], book_id: int = -1):
        self.books: list[tuple[Book, BookStats]] = books
        self.book_id = book_id

    def __str__(self):
        s = f"------\nAccountingApp:\nBookId: {self.book_id}\nBooks:\n"
        s += U.print_list(self.books, mute=True)
        s += "------"
        return s

    @property
    def current_book(self):
        if len(self.books) <= 0:  # create a new book if there's no book while looking for current book
            self.create_book("我的账本")
            self.book_id = 0
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

    def _setactivate_book(self, name, activate, **kwargs):
        book = None
        if "book" in kwargs:
            book = kwargs["book"]
        
        for b, s in self.books:
            if book is not None and b == book:
                s.activated = activate
                break
            elif b.name == name:
                s.activated = activate
                break

    def deactivate_book(self, name: str = None, **kwargs):
        self._setactivate_book(name, False, **kwargs)

    def activate_book(self, name: str = None, **kwargs):
        self._setactivate_book(name, True, **kwargs)

    def current_items(self, key: Callable[..., bool] = None, sort_key: Callable = None, sort_descending: bool = True, **kwargs):
        return self.current_book.select_items(key, sort_key, sort_descending, **kwargs)

    def append_item(self, type: U.AccountItemType | str, name: str, amount: float, time: datetime = None, **kwargs):
        self.current_book.create_item(type, name, amount, time, **kwargs)

    def edit_item(self, item: AccountItem, to_type = None, to_name = None, to_amount = None, to_time = None, **kwargs):
        self.current_book.edit_item(item, to_type, to_name, to_amount, to_time, **kwargs)

    def delete_item(self, item: AccountItem):
        self.current_book.delete_item(item)
    
    def sort_items(self, key: Callable = None, descending: bool = True, items_list: list[AccountItem] = None):
        """使用 `items_list` 参数，则返回排序后的列表；否则只对当前账本中的账目排序，无返回值"""
        if isinstance(items_list, list):
            return sorted(items_list, key=key, reverse=descending) if key is not None else items_list
        self.current_book.sort_items(key=key, descending=descending)
        return None

    def select_items(self, key: Callable[..., bool] = None, sort_key: Callable = None, sort_descending: bool = True, items_list: list[AccountItem] = None, **kwargs):
        """使用 `items_list` 参数，则从给定列表中选择；否则只从当前账本的账目中选择"""
        if not isinstance(items_list, list):
            return self.current_book.select_items(key, sort_key, sort_descending, **kwargs)

        selected = [] if key is not None else items_list
        if len(selected) <= 0:
            for item in items_list:
                if key(item, **kwargs):
                    selected.append(item)
        if sort_key is not None:
            selected = sorted(selected, key=sort_key, reverse=sort_descending)
        return selected

    def merge_selected_items(self, to_union: bool = False, *selected_items: list[AccountItem]):
        """将多个根据不同条件选取的账目列表取交集/并集"""
        merged = set()
        for items in selected_items:
            if to_union:
                merged = merged & set(items)
            else:
                merged = merged | set(items)
        return list(merged)

    def addup(self, key: Callable[..., bool] = None, to_info: bool = False, items_list: list[AccountItem] = None, **kwargs):
        if isinstance(items_list, list):
            selections: list[AccountItem] = self.select_items(key=key, items_list=items_list, **kwargs)
            amount = 0.0
            for item in selections:
                amount += item.amount
        else:
            amount = self.current_book.addup(key=key, **kwargs)

        if not to_info:
            return amount
        else:
            return ("+" if amount > 0 else "") + f"{amount:.2f}"

    def inout_daily(self, year: int = None, month: int = None, day: int = None, to_info: bool = False):
        return self.addup(key=BookItemSelectKeys.SpecificDay, to_info=to_info, year=year, month=month, day=day)
    
    def inout_monthly(self, year: int = None, month: int = None, to_info: bool = False):
        return self.addup(key=BookItemSelectKeys.SpecificMonth, to_info=to_info, year=year, month=month)
    
    def inout_yearly(self, year: int = None, to_info: bool = False):
        return self.addup(key=BookItemSelectKeys.SpecificYear, to_info=to_info, year=year)


class AccountingAppJson(json.JSONEncoder):
    def __init__(self, *, skipkeys = False, ensure_ascii = True, check_circular = True, allow_nan = True, sort_keys = False, indent = None, separators = None, default = None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators, default=default)

    def default(self, o):
        if isinstance(o, AccountingApp):
            return AccountingAppJson.encode_dict(o)
        return super().default(o)

    @staticmethod
    def encode_dict(o: AccountingApp):
        books = []
        for b, s in o.books:
            b = BookJson.encode_dict(b)
            s = BookStatsJson.encode_dict(s)
            books.append((b, s))
        return {
            "books": books,
            "book_id": o.book_id,
        }

    @staticmethod
    def decode(d):
        books = []
        books_dict = d["books"]
        for bs in books_dict:
            book = bs[0]
            book = BookJson.decode(book)
            stats = bs[1]
            stats = BookStatsJson.decode(stats)
            books.append((book, stats))
        book_id = d["book_id"]
        app = AccountingApp(books, book_id)
        return app


def load_app(save_json: str = None) -> AccountingApp:
    if save_json is not None:
        # print(f"Loaded app saved data")
        saved = json.loads(save_json)
        return AccountingAppJson.decode(saved)
    return AccountingApp()


if __name__ == "__main__":
    # test: app save and load
    app = load_app()
    print(app)
    app.create_book("b1")
    app.create_book("b2")
    app.switch_book(0)
    app.append_item("Books", "haha", 14)
    app.append_item("Clothes", "lol", 200.3)
    app.switch_book(1)
    app.append_item("Health", "sdkf", 155.5)
    print(app)
    appsave = json.dumps(app, cls=AccountingAppJson)
    print(appsave)
    app2 = load_app(appsave)
    print(f"app2:\n{app2}")
    U.print_list(app2.books[0][0].items)
    U.print_list(app2.books[1][0].items)
    exit()

    # test: json
    a = AccountItem("Books", "lol", 114.5)
    print(a)
    s = json.dumps(a, cls=AccountItemJson)
    print(s)
    b = json.loads(s)
    print(b)
    b = AccountItemJson.decode(b)
    print(b)

    b1 = Book("a")
    b1.create_item("Books", "haha", 114.5)
    b1.create_item("Clothes", "lol", 14.0)
    ss = json.dumps(b1, cls=BookJson)
    print(ss)
    b2 = json.loads(ss)
    b2 = BookJson.decode(b2)
    print(b2)
    U.print_list(b2.items)
    exit()

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

    # test: create and edit item
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
    U.print_list(b1.select_items(key=BookItemSelectKeys.TimeRange, sort_key=BookItemSortKeys.Time, start=datetime(2025, 2, 1), end=datetime(2025, 4, 1)))

    # test: addup
    print("----------")
    print(f"all: {b1.addup()}")
    print(f"books: {b1.addup(key=BookItemSelectKeys.Type, type="Books")}")
    print(f"feb to apr: {b1.addup(key=BookItemSelectKeys.TimeRange, start=datetime(2025, 2, 1), end=datetime(2025, 4, 1))}")