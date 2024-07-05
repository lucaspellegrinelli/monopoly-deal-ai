from typing import List

from monopoly.enums.action_type import ActionType
from monopoly.enums.property_color import PropertyColor


# Class responsible for managing what a general card should have
class Card:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Money Card
class MoneyCard(Card):
    def __init__(self, name: str, value: int):
        Card.__init__(self, name, value)


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Action Card (examples of Action Cards are like 'Deal Breaker' or
# 'Debt Collector')
class ActionCard(MoneyCard):
    def __init__(self, name: str, value: int, action: ActionType):
        Card.__init__(self, name, value)
        self.action = action


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Rent Card (including multiple colors rent and wild rent)
class RentCard(MoneyCard):
    def __init__(
        self,
        name: str,
        value: int,
        colors: List[PropertyColor],
        is_wild: bool,
    ):
        Card.__init__(self, name, value)
        self.colors = colors
        self.is_wild = is_wild


# Class responsible for managing what (besides what's already defined in the Card class)
# is necessary for a Property Card (that could have multiple colors)
class PropertyCard(Card):
    def __init__(self, name: str, value: int, colors: List[PropertyColor]):
        Card.__init__(self, name, value)
        self.colors = colors

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.value == other.value
            and self.colors == other.colors
        )


# Class corresponding to a card that the target player doesn't have information about
# like in the case of other players hand or the deck
class UnknownCard(Card):
    def __init__(self):
        Card.__init__(self, "Unknown", -1)
