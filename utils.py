from enum import IntEnum, Enum


def print_list(l: list, depth: int = 0):
    prefix = "".join(["  " for _ in range(depth)])

    if not isinstance(l, list):
        print(f"{prefix}{str(l)}")
        return
    
    print(f"{prefix}[")
    for elem in l:
        print_list(elem, depth + 1)
    print(f"{prefix}]")


class AccountItemType:
    def __init__(self, icon: str, name: str, *namealt: str):
        self.icon = icon
        self.name = name
        self.namealt = namealt

    def __str__(self):
        return str((self.icon, self.name, *self.namealt))


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


if __name__ == "__main__":
    print(str(AccountItemTypes.Electronics))
    AccountItemTypes.create_custom_type("🐂", "牛牛", "cow cow")
    print_list(AccountItemTypes.CustomTypes)
    AccountItemTypes.modify_custom_type("你好", "", "")
    AccountItemTypes.modify_custom_type("牛牛", "🐄", "nn", "cccow cccow")
    print_list(AccountItemTypes.CustomTypes)
    AccountItemTypes.delete_custom_type("nn")
    print_list(AccountItemTypes.CustomTypes)