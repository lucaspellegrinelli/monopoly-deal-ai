from typing import List

from monopoly.enums.action_type import ActionType
from monopoly.enums.property_color import PropertyColor
from monopoly.models.card import ActionCard, Card, MoneyCard, PropertyCard, RentCard

ALL_CARDS: List[Card] = []

# ============================= MONEY ============================= #

MONEY_CARDS = [
    [MoneyCard("10M", 10) for _ in range(1)],
    [MoneyCard("5M", 5) for _ in range(2)],
    [MoneyCard("4M", 4) for _ in range(3)],
    [MoneyCard("3M", 3) for _ in range(3)],
    [MoneyCard("2M", 2) for _ in range(5)],
    [MoneyCard("1M", 1) for _ in range(6)],
]

for money_card in MONEY_CARDS:
    ALL_CARDS += money_card


# ============================= PROPERTY ============================= #

PROPERTY_CARDS = [
    [PropertyCard("Brown Property", 1, [PropertyColor.BROWN]) for _ in range(2)],
    [
        PropertyCard("Dark Blue Property", 4, [PropertyColor.DARK_BLUE])
        for _ in range(2)
    ],
    [
        PropertyCard("Light Green Property", 2, [PropertyColor.LIGHT_GREEN])
        for _ in range(2)
    ],
    [PropertyCard("Green Property", 4, [PropertyColor.GREEN]) for _ in range(3)],
    [
        PropertyCard("Light Blue Property", 1, [PropertyColor.LIGHT_BLUE])
        for _ in range(3)
    ],
    [PropertyCard("Orange Property", 2, [PropertyColor.ORANGE]) for _ in range(3)],
    [PropertyCard("Pink Property", 2, [PropertyColor.PINK]) for _ in range(3)],
    [PropertyCard("Red Property", 3, [PropertyColor.RED]) for _ in range(3)],
    [PropertyCard("Yellow Property", 3, [PropertyColor.YELLOW]) for _ in range(3)],
    [PropertyCard("Black Property", 2, [PropertyColor.BLACK]) for _ in range(4)],
    [
        PropertyCard(
            "Dark Blue/Green Property",
            4,
            [PropertyColor.DARK_BLUE, PropertyColor.GREEN],
        )
        for _ in range(1)
    ],
    [
        PropertyCard(
            "Light Blue/Brown Property",
            1,
            [PropertyColor.LIGHT_BLUE, PropertyColor.BROWN],
        )
        for _ in range(1)
    ],
    [
        PropertyCard(
            "Black/Green Property", 4, [PropertyColor.BLACK, PropertyColor.GREEN]
        )
        for _ in range(1)
    ],
    [
        PropertyCard(
            "Light Blue/Black Property",
            4,
            [PropertyColor.LIGHT_BLUE, PropertyColor.BLACK],
        )
        for _ in range(1)
    ],
    [
        PropertyCard(
            "Black/Light Green Property",
            2,
            [PropertyColor.BLACK, PropertyColor.LIGHT_GREEN],
        )
        for _ in range(1)
    ],
    [
        PropertyCard(
            "Pink/Orange Property", 2, [PropertyColor.PINK, PropertyColor.ORANGE]
        )
        for _ in range(2)
    ],
    [
        PropertyCard(
            "Red/Yellow Property", 3, [PropertyColor.RED, PropertyColor.YELLOW]
        )
        for _ in range(2)
    ],
    [PropertyCard("Rainbow Property", 0, [PropertyColor.RAINBOW]) for _ in range(2)],
]

for property_card in PROPERTY_CARDS:
    ALL_CARDS += property_card

# ============================= RENT ============================= #

RENT_CARDS = [
    [
        RentCard(
            "Dark Blue/Green Rent",
            1,
            [PropertyColor.GREEN, PropertyColor.DARK_BLUE],
            False,
        )
        for _ in range(2)
    ],
    [
        RentCard(
            "Brown/Light Blue Rent",
            1,
            [PropertyColor.BROWN, PropertyColor.LIGHT_BLUE],
            False,
        )
        for _ in range(2)
    ],
    [
        RentCard(
            "Pink/Orange Rent", 1, [PropertyColor.PINK, PropertyColor.ORANGE], False
        )
        for _ in range(2)
    ],
    [
        RentCard(
            "Black/Light Green Rent",
            1,
            [PropertyColor.BLACK, PropertyColor.LIGHT_GREEN],
            False,
        )
        for _ in range(2)
    ],
    [
        RentCard("Red/Yellow Rent", 1, [PropertyColor.RED, PropertyColor.YELLOW], False)
        for _ in range(2)
    ],
    [RentCard("Wild Rent", 1, [], True) for _ in range(3)],
]

for rent_card in RENT_CARDS:
    ALL_CARDS += rent_card

# ============================= ACTIONS ============================= #

ACTION_CARDS = [
    [ActionCard("Deal Breaker", 5, ActionType.DEAL_BREAKER) for _ in range(2)],
    [ActionCard("Debt Collector", 3, ActionType.DEBT_COLLECTOR) for _ in range(3)],
    [ActionCard("Double the Rent", 1, ActionType.DOUBLE_RENT) for _ in range(2)],
    [ActionCard("Forced Deal", 3, ActionType.FORCED_DEAL) for _ in range(4)],
    [ActionCard("Hotel", 4, ActionType.HOTEL) for _ in range(3)],
    [ActionCard("House", 3, ActionType.HOUSE) for _ in range(3)],
    [ActionCard("It's my birthday", 2, ActionType.ITS_MY_BIRTHDAY) for _ in range(3)],
    [ActionCard("Just Say No", 4, ActionType.JUST_SAY_NO) for _ in range(3)],
    [ActionCard("Pass Go", 1, ActionType.PASS_GO) for _ in range(10)],
    [ActionCard("Sly Deal", 3, ActionType.SLY_DEAL) for _ in range(3)],
]

for action_card in ACTION_CARDS:
    ALL_CARDS += action_card
