from typing import List

from monopoly.enums.action_type import ActionType
from monopoly.enums.property_color import PropertyColor


# Class responsible for managing what a general card should have
class Card:
    def __init__(self, id: int, name: str, value: int):
        self.id = id
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Money Card
class MoneyCard(Card):
    def __init__(self, id: int, name: str, value: int):
        Card.__init__(self, id, name, value)


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Action Card (examples of Action Cards are like 'Deal Breaker' or
# 'Debt Collector')
class ActionCard(Card):
    def __init__(self, id: int, name: str, value: int, action: ActionType):
        Card.__init__(self, id, name, value)
        self.action = action


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Property Card (that could have multiple colors)
class PropertyCard(Card):
    def __init__(self, id: int, name: str, value: int, colors: List[PropertyColor]):
        Card.__init__(self, id, name, value)
        self.colors = colors

    def isRainbow(self):
        return any(color == PropertyColor.RAINBOW for color in self.colors)


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Rent Card (including multiple colors rent and wild rent)
class RentCard(Card):
    def __init__(
        self,
        id: int,
        name: str,
        value: int,
        colors: List[PropertyColor],
        is_wild: bool,
    ):
        Card.__init__(self, id, name, value)
        self.colors = colors
        self.is_wild = is_wild


# Class corresponding to a card that the target player doesn't have information about
# like in the case of other players hand or the deck
class UnknownCard(Card):
    def __init__(self):
        Card.__init__(self, -1, "Unknown", -1)
