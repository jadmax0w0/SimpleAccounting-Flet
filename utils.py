from enum import IntEnum, Enum
import random
from datetime import datetime
from json import JSONEncoder


def print_list(l: list, depth: int = 0):
    prefix = "".join(["  " for _ in range(depth)])

    if not isinstance(l, list):
        print(f"{prefix}{str(l)}")
        return
    
    print(f"{prefix}[")
    for elem in l:
        print_list(elem, depth + 1)
    print(f"{prefix}]")


def random_datetime(year = True, month = True, day = True, hour = True):
    if isinstance(year, bool) and year is True:
        y = random.randint(1000, 3000)
    elif isinstance(year, tuple):
        y = random.choice(year)
    elif isinstance(year, int):
        y = year

    if isinstance(month, bool) and month is True:
        m = random.randint(1, 12)
    elif isinstance(month, tuple):
        m = random.choice(month)
    elif isinstance(month, int):
        m = month

    if isinstance(day, bool) and day is True:
        d = random.randint(1, 28)
    elif isinstance(day, tuple):
        d = random.choice(day)
    elif isinstance(day, int):
        d = day

    if isinstance(hour, bool) and hour is True:
        h = random.randint(0, 23)
    elif isinstance(hour, tuple):
        h = random.choice(hour)
    elif isinstance(hour, int):
        h = hour

    return datetime(year=y, month=m, day=d, hour=h)


class AccountItemType:
    def __init__(self, icon: str, name: str, *namealt: str):
        self.icon = icon
        self.name = name
        self.namealt = namealt

    def __str__(self):
        return "AccountItemType: " + str((self.icon, self.name, *self.namealt))
    
    def __eq__(self, value):
        if isinstance(value, AccountItemType):
            return self.icon == value.icon and self.name == value.name and self.namealt == self.namealt
        elif isinstance(value, str):
            return self.name == value or value in self.namealt
        else:
            return False


class AccountItemTypes:
    FoodDrink = AccountItemType("🍔", "饮食", "Food and Drink")
    Clothes = AccountItemType("👗", "衣服", "Clothes")
    Electronics = AccountItemType("💻", "电子", "Electronics")
    Lifestyle = AccountItemType("🕶️", "生活", "Lifestyle")
    Health = AccountItemType("🩺", "医药", "Health")
    Entertainment = AccountItemType("🎱", "娱乐", "Entertainment")
    Games = AccountItemType("🎮", "游戏", "Games")
    Study = AccountItemType("🖊️", "学习", "Study")
    Books = AccountItemType("📖", "书籍", "Books")
    Utility = AccountItemType("🛠️", "杂务", "Utility")
    Virtual = AccountItemType("💳", "虚拟", "Virtual")
    Others = AccountItemType("✨", "其他", "Others")

    CustomTypes: list[AccountItemType] = [
        FoodDrink, Clothes, Electronics, Lifestyle, Health, Entertainment, Games, Study, Books, Utility, Virtual, Others
    ]

    @staticmethod
    def create_custom_type(icon: str, name: str, *namealt: str, **kwargs):
        entry = None
        if "entry" in kwargs:
            entry = kwargs["entry"]
        else:
            entry = AccountItemType(icon, name, *namealt)
        assert entry is not None

        for e in AccountItemTypes.CustomTypes:
            assert e.name != entry.name  # no duplicate names
        AccountItemTypes.CustomTypes.append(entry)

    @staticmethod
    def delete_custom_type(name: str, **kwargs):
        entry = None
        if "entry" in kwargs:
            entry = kwargs["entry"]
        if entry not in AccountItemTypes.CustomTypes:
            for e in AccountItemTypes.CustomTypes:
                if e.name == name:
                    entry = e
                    break
            if entry not in AccountItemTypes.CustomTypes:
                print(f"Warning: no item type named \"{name}\" found in custom types list")
                return
        
        AccountItemTypes.CustomTypes.remove(entry)

    @staticmethod
    def modify_custom_type(target_name: str, to_icon: str, to_name: str, *to_namealt: str, **kwargs):
        from_entry_id = -1
        for i in range(len(AccountItemTypes.CustomTypes)):
            e = AccountItemTypes.CustomTypes[i]
            if e.name == target_name:
                from_entry_id = i
                break
        if not (from_entry_id >= 0 and from_entry_id < len(AccountItemTypes.CustomTypes)):
            print(f"Warning: no item type named \"{target_name}\" found in custom types list")
            return

        to_entry = None
        if "to_entry" in kwargs:
            to_entry = kwargs["to_entry"]
        else:
            to_entry = AccountItemType(to_icon, to_name, *to_namealt)
        assert to_entry is not None

        AccountItemTypes.CustomTypes[from_entry_id] = to_entry


class AccountItemTypeJson(JSONEncoder):
    def __init__(self, *, skipkeys = False, ensure_ascii = True, check_circular = True, allow_nan = True, sort_keys = False, indent = None, separators = None, default = None):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators, default=default)

    def default(self, o):
        if isinstance(o, AccountItemType):
            return o.__dict__
        return super().default(o)


if __name__ == "__main__":
    print(str(AccountItemTypes.Electronics))
    AccountItemTypes.create_custom_type("🐂", "牛牛", "cow cow")
    print_list(AccountItemTypes.CustomTypes)
    AccountItemTypes.modify_custom_type("你好", "", "")
    AccountItemTypes.modify_custom_type("牛牛", "🐄", "nn", "cccow cccow")
    print_list(AccountItemTypes.CustomTypes)
    AccountItemTypes.delete_custom_type("nn")
    print_list(AccountItemTypes.CustomTypes)