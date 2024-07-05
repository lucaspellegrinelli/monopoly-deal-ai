import sys

sys.path.append("../")

import random

from monopoly.ai import AI
from monopoly.models.action import (
    AskMoneyAction,
    MovePropertyAction,
    PlayPropertyAction,
    StealPropertyAction,
    StealPropertySetAction,
    SwapPropertyAction,
)
from monopoly.models.property_set import PropertySet


# Example of an implemented AI that does random stuff for living
class RandomAI(AI):

    def choose_move(self, instance, player_id, moves_left):
        possible_moves = instance.get_turn_possible_moves(instance.get_player(player_id))
        return possible_moves[random.randint(0, len(possible_moves) - 1)]

    def choose_payment(
        self, instance, player_id, player_sets, player_money_pile, how_much
    ):
        payment = []
        payed = 0

        for item in player_money_pile:
            if payed < how_much:
                payed += item.value
                payment.append(item)

        for p_set in player_sets:
            for item in p_set.properties:
                if payed < how_much:
                    payed += item.value
                    payment.append(item)
                else:
                    break

        return payment

    def choose_what_to_discard(self, instance, player_id, player_hand):
        discarded = []
        while len(player_hand) > 7:
            discarded.append(player_hand.pop(random.randint(0, len(player_hand) - 1)))
        return discarded

    def recieve_properties_from_payment(self, instance, player_id, properties):
        player = instance.get_player(player_id)
        actions = []

        for item in properties:
            added = False
            for pSet in player.sets:
                if pSet.can_add_property(item):
                    actions.append(PlayPropertyAction(player, item, pSet))
                    added = True
                    break

            if not added:
                actions.append(
                    PlayPropertyAction(player, item, PropertySet(item.colors))
                )

        return actions

    def will_negate(self, instance, player_id, action):
        if isinstance(action, AskMoneyAction):
            return True
        elif isinstance(action, StealPropertyAction):
            return False
        elif isinstance(action, StealPropertySetAction):
            return True
        elif isinstance(action, SwapPropertyAction):
            return False
        else:
            return False

    def rearrange_cards(self, instance, player_id, player_sets):
        actions = []
        wild_cards = []
        for pset in player_sets:
            if not pset.is_color_defined():
                wild = (pset.properties[0], pset)
                wild_cards.append(wild)

        for wild in wild_cards:
            added = False
            for set in player_sets:
                if set.can_add_property(wild[0]):
                    actions.append(MovePropertyAction(player_id, wild[0], wild[1], set))
                    break

        return actions
