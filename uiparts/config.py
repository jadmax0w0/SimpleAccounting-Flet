import flet as ft


class UIConfig:
    # title card
    BookTitleTextSize = 25

    BookTitleTextWeight = ft.FontWeight.BOLD  # 600

    TitleYearTextSize = 20
    TitleMonthTextSize = 15
    TitleMonthTextWight = ft.FontWeight.BOLD  # 500
    TitleMonthTextWidth = 300
    TitleMonthTextExpand = 3

    TitleTypesTextExpand = 4
    TitleInoutTextSize = 15
    TitleInoutTextWeight = ft.FontWeight.BOLD  # 600
    TitleInoutTextExpand = 2
    TitleColumnSpacing = 15
    TitleRowSpacing = 15

    TitleCardWidth = None
    TitleCardHeight = 185
    TitleCardInnerPadding = ft.Padding(30, 15, 30, 15)
    
    # item list
    ItemYearMonthTextSize = 20
    ItemYearMonthTextWeight = ft.FontWeight.BOLD  # 600
    ItemYearMonthPadding = 15
    ItemTextSize = 15
    ItemTextWeight = ft.FontWeight.NORMAL  # 400
    ItemIconWidth = 20
    ItemNameWidth = 150
    ItemTimeWidth = 300
    ItemAmountWidth = 100
    ItemListPadding = ft.Padding(15, 0, 15, 80)  # BottomRowHeight
    ItemListSpacing = 15
    ItemListWidth = None

    EmptyItemsHintWidth = 300
    EmptyItemsHintPadding = ft.Padding(0, 0, 0, 80)  # BottomRowHeight

    # bottom bar
    TypesListHeight = 35
    TypesListSpacing = 15
    TypeButtonWidth = 65
    TypeButtonColor = ft.Colors.PRIMARY, ft.Colors.PRIMARY_CONTAINER
    TypeButtonColorSelected = ft.Colors.ON_PRIMARY, ft.Colors.ON_PRIMARY_CONTAINER
    CreateItemButtonWidth = 60
    CreateItemButtonHeight = 60
    BottomRowPadding = ft.Padding(10, 0, 10, 0)
    BottomRowWidth = None
    BottomRowHeight = 80
    BottomRowBlur = 10

    # main column
    MainPadding = 15