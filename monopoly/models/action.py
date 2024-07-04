from typing import List

from monopoly.models.card import ActionCard, MoneyCard, PropertyCard
from monopoly.models.property_set import PropertySet


class Action:
    def __init__(self, who_used_id: int):
        self.who_used_id = who_used_id


# Class representing the action of not playing any cards
class DoNothingAction(Action):
    def __init__(self, who_used_id: int):
        Action.__init__(self, who_used_id)

    def __repr__(self):
        return "Nothing"


# Class representing the action of a target player playing a property
# into a property set
class PlayPropertyAction(Action):
    def __init__(
        self, who_used_id: int, property: PropertyCard, property_set: PropertySet
    ):
        Action.__init__(self, who_used_id)
        self.property = property
        self.property_set = property_set

    def __repr__(self):
        name = self.property.name
        size = len(self.property_set.properties)
        return f"Played {name} into a pSet with {size} properties"


# Class representing the action of a target player moving a property
# between two property sets
class MovePropertyAction(Action):
    def __init__(
        self,
        who_used_id: int,
        property: PropertyCard,
        property_set_bef: PropertySet,
        property_set_aft: PropertySet,
    ):
        Action.__init__(self, who_used_id)
        self.property = property
        self.property_set_bef = property_set_bef
        self.property_set_aft = property_set_aft

    def __repr__(self):
        name = self.property.name
        b_size = len(self.property_set_bef.properties)
        a_size = len(self.property_set_aft.properties)
        return f"Moved {name} from a pSet with {b_size} properties to a pSet with {a_size} properties"


# Class representing the action of a target player adding a card to
# its money pile
class AddMoneyAction(Action):
    def __init__(self, who_used_id: int, money: MoneyCard):
        Action.__init__(self, who_used_id)
        self.money = money

    def __repr__(self):
        return f"Added {self.money} to the money pile"


# Class representing the action of a target player resolving the effect
# of a card that requires one or more other players to give it a specified
# amount of money
class AskMoneyAction(Action):
    def __init__(
        self,
        who_used_id: int,
        action_card: ActionCard,
        money: MoneyCard,
        target_ids: List[int],
    ):
        Action.__init__(self, who_used_id)
        self.action_card = action_card
        self.money = money
        self.target_ids = target_ids

    def __repr__(self):
        return f"Asked {self.money} for Players {self.target_ids}"


# Class representing the action of a target player drawing a specific
# amount of cards
class DrawCardsAction(Action):
    def __init__(self, who_used_id: int, action_card: ActionCard, quantity: int):
        Action.__init__(self, who_used_id)
        self.action_card = action_card
        self.quantity = quantity

    def __repr__(self):
        return f"Drew {self.quantity} cards"


# Class representing the action of a target player adding a house or hotel
# on top of a specified property set
class AddHouseHotelAction(Action):
    def __init__(
        self,
        who_used_id: int,
        action_card: ActionCard,
        property_set: PropertySet,
        is_adding_house: bool,
    ):
        Action.__init__(self, who_used_id)
        self.action_card = action_card
        self.property_set = property_set
        self.is_adding_house = is_adding_house

    def __repr__(self):
        added = "House" if self.is_adding_house else "Hotel"
        return f"Added a {added} to a set"


# Class representing the action of a target player resolving the effect
# of a card that steals a specified property from another player
class StealPropertyAction(Action):
    def __init__(
        self,
        who_used_id: int,
        action_card: ActionCard,
        property: PropertyCard,
        other_player_id: int,
    ):
        Action.__init__(self, who_used_id)
        self.action_card = action_card
        self.property = property
        self.other_player_id = other_player_id

    def __repr__(self):
        return (
            f"Stole {self.property.name} property from player #{self.other_player_id}"
        )


# Class representing the action of a target player resolving the effect
# of a card that steals a specified property set from another player
class StealPropertySetAction(Action):
    def __init__(
        self,
        who_used_id: int,
        action_card: ActionCard,
        property_set: PropertySet,
        other_player_id: int,
    ):
        Action.__init__(self, who_used_id)
        self.action_card = action_card
        self.property_set = property_set
        self.other_player_id = other_player_id

    def __repr__(self):
        stole_count = len(self.property_set.properties)
        return f"Stole pSet with {stole_count} properties from player #{self.other_player_id}"


# Class representing the action of a target player resolving the effect
# of a card that swaps a specified property with another player
class SwapPropertyAction(Action):
    def __init__(
        self,
        who_used_id: int,
        action_card: ActionCard,
        my_property: PropertyCard,
        other_property: PropertyCard,
        other_player_id: int,
    ):
        Action.__init__(self, who_used_id)
        self.action_card = action_card
        self.my_property = my_property
        self.other_property = other_property
        self.other_player_id = other_player_id

    def __repr__(self):
        return f"Swapped {self.my_property.name} to {self.other_property.name} (from Player #{self.other_player_id})"


# Class representing the action of a target player resolving the effect
# of a card that doubles the amount of money that a rent card would require
# from other players
class ApplyDoubleRent(Action):
    def __init__(self, who_used_id: int, action_card: ActionCard):
        Action.__init__(self, who_used_id)
        self.action_card = action_card

    def __repr__(self):
        return "Applied Double Rent"
