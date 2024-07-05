import copy
from typing import List

from monopoly.ai import AI
from monopoly.enums.action_type import ActionType
from monopoly.models.action import (
    Action,
    DoNothingAction,
    MovePropertyAction,
    PlayPropertyAction,
)
from monopoly.models.card import ActionCard, Card, MoneyCard, PropertyCard, RentCard
from monopoly.models.property_set import PropertySet


class Player:
    def __init__(self, id: int, name: str, hand: List[Card], ai: AI):
        self.id = id
        self.name = name
        self.hand = hand
        self.ai = ai

        self.sets: List[PropertySet] = []
        self.money: List[MoneyCard] = []

        self.double_rent = False
        self.max_cards_in_hand = 7

    # Calls the AI with all the game instance so that the player will choose
    # which action it will take in its turn
    def choose_move(self, instance, moves_left: int):
        move = self.ai.choose_move(instance, self.id, moves_left)

        if not isinstance(move, Action):
            move = DoNothingAction(self.id)

        return move

    # Calls the AI so that the player will choose which of its cards will be
    # used as payment to a rent or action card used against him
    def choose_payment(self, instance, how_much: int):
        payment = []
        payed = 0

        while payed < how_much and len(self.money) > 0 and len(self.sets) > 0:
            this_it_pay = self.ai.choose_payment(
                instance, self.id, self.sets, self.money, how_much
            )

            if len(this_it_pay) == 0:
                raise RuntimeError(
                    "The method 'choosePayment' didn't choose enough cards \
        to pay the required amount even tough it has more cards and in this iteration \
        it didn't return any cards. This might be a sign of an infinite loop where \
        'choosePayment' will never finish to choose the payment since it will not \
        make any more actions (based on the fact that in this iteration it didn't)."
                )

            payment += this_it_pay

            for card in payment:
                payed += card.value
                if isinstance(card, PropertyCard):
                    for set in self.sets:
                        if set.has_property(card):
                            set.remove_property(card)
                            break
                else:
                    self.remove_from_money_pile(card)

        return payment

    # Calls the AI so that the player will choose which of its cards will be
    # discarded as a result of having more that the allowed cards in its hand
    def choose_what_to_discard(self, instance):
        discarded = []
        while len(self.hand) > self.max_cards_in_hand:
            discarded += self.ai.choose_what_to_discard(instance, self.id, self.hand)

            if len(discarded) == 0:
                raise RuntimeError(
                    "You didn't discard enough in the 'chooseWhatToDiscard' \
        and in this iteration the discard list is empty. This might be a \
        sign of an infinite loop where 'chooseWhatToDiscard' will never finish to \
        discard the necessary cards since it will not make any more actions (based \
        on the fact that in this iteration it didn't)."
                )

            for card in discarded:
                self.remove_from_hand(card)

        return discarded

    # Calls the AI so it decides where to put all of the properties/money it has recieved
    # as a result of using a card that asks for a payment
    def recieve_payment(self, instance, payment: List[Card]):
        single_properties: List[PropertyCard] = []
        for item in payment:
            if (
                isinstance(item, MoneyCard)
                or isinstance(item, ActionCard)
                or isinstance(item, RentCard)
            ):
                self.money.append(item)
            elif isinstance(item, PropertyCard):
                single_properties.append(item)
            elif isinstance(item, PropertySet):
                self.sets.append(item)

        if single_properties:
            actions = self.ai.recieve_properties_from_payment(
                instance, self.id, single_properties
            )

            if len(actions) == 0:
                raise RuntimeError(
                    "There are properties unaddressed in 'recievePayment' \
        and in this iteration the method didn't make any actions. This might be a \
        sign of an infinite loop where 'recievePayment' will never finish to \
        address all the properties since it will not make any more actions (based \
        on the fact that in this iteration it didn't)."
                )

            addressed_cards: List[Card] = []
            for action in actions:
                if isinstance(action, PlayPropertyAction):
                    property_recieved = False
                    for card in single_properties:
                        if card == action.property:
                            property_recieved = True
                            break

                    if property_recieved:
                        addressed_cards.append(action.property)
                        self.give_property_to_set(action.property_set, action.property)
                    else:
                        raise RuntimeError(
                            "In 'recievePayment' you tried to play a property \
            you didn't recieve."
                        )
                else:
                    raise RuntimeError(
                        "In 'recievePayment' you returned an action that is not \
          of the type PlayPropertyAction."
                    )

            addressed_card_names = set([c.name for c in addressed_cards])
            unaddressed_cards = [
                p for p in single_properties if p.name not in addressed_card_names
            ]

            if len(unaddressed_cards) > 0:
                self.ai.recieve_properties_from_payment(
                    instance, self.id, unaddressed_cards
                )

    # Calls the AI so that the player can decide if (given it has a "JUST SAY NO" card) it
    # wants to negate or not a card used against him.
    def will_negate(self, instance, action: Action):
        actions = [c for c in self.hand if isinstance(c, ActionCard)]
        has_negate = any([c for c in actions if c.action == ActionType.JUST_SAY_NO])

        if has_negate:
            negate = self.ai.will_negate(instance, self.id, action)
            if negate != True and negate != False:
                raise RuntimeError(
                    "In the 'willNegate' method, the return value was not a boolean."
                )
            return negate
        else:
            return False

    # Calls the AI to decide how it wants to be arranged.
    def rearrange_cards(self, instance):
        actions = []
        r = self.ai.rearrange_cards(instance, self.id, self.sets)
        for action in r:
            if isinstance(action, MovePropertyAction):
                actions.append(action)
            else:
                raise RuntimeError(
                    "In 'rearrangeCards' you returned an action that is not \
        of the type PlayPropertyAction."
                )
        return actions

    def pass_turn(self):
        self.double_rent = False
        self.clean_clear_sets()

    def clean_clear_sets(self):
        self.sets = [x for x in self.sets if x.number_of_properties() > 0]

    def has_won(self, how_many_to_win: int):
        completed = 0
        for set in self.sets:
            if set.is_completed():
                completed += 1

        return completed >= how_many_to_win

    # ======================== CARD MANAGEMENT ========================

    def give_property_to_set(self, pset: PropertySet, card: PropertyCard):
        if pset.number_of_properties() > 0:
            for s in self.sets:
                if s == pset:
                    s.add_property(card)
                    return
        else:
            pSet = PropertySet(pset.colors)
            pSet.add_property(card)
            self.add_property_set(pSet)

    def take_out_property(self, property: PropertyCard):
        for set in self.sets:
            if set.has_property(property):
                set.remove_property(property)
                return

    def add_to_hand(self, cards: List[Card]):
        self.hand += cards

    def remove_from_hand(self, card: Card):
        # TODO: MAKE THIS WORK WITH "self.hand.remove(card)"
        # where instead of looping through the hand and finding
        # the correct card, I can just pass the 'card' parameter
        # and based on its id, the correct card is removed
        for c in self.hand:
            if c == card:
                self.hand.remove(c)
                break

    def add_property_set(self, pset: PropertySet):
        self.sets.append(pset)

    def has_property_set(self, pset: PropertySet):
        return pset in self.sets

    def remove_property_set(self, pset: PropertySet):
        self.sets.remove(pset)

    def add_to_money_pile(self, card: MoneyCard):
        self.money.append(card)

    def remove_from_money_pile(self, card: MoneyCard):
        # TODO: MAKE THIS WORK WITH "self.money.remove(card)"
        # where instead of looping through the hand and finding
        # the correct card, I can just pass the 'card' parameter
        # and based on its id, the correct card is removed
        for c in self.money:
            if c == card:
                self.money.remove(c)
                break

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        final = "\n- Hand :\t" + str(self.hand) + "\n"
        final += "- Money:\t" + str(self.money) + "\n"
        final += "- Field:\t" + str(self.sets) + "\n"

        return final

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False

        return self.id == other.id
