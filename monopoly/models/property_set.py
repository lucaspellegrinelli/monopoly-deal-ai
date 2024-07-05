import uuid
from typing import List

from monopoly.enums.property_color import PropertyColor

RENT_VALUE = {
    PropertyColor.BROWN: [1, 2],
    PropertyColor.DARK_BLUE: [3, 8],
    PropertyColor.GREEN: [2, 4, 7],
    PropertyColor.LIGHT_BLUE: [1, 2, 3],
    PropertyColor.ORANGE: [1, 3, 5],
    PropertyColor.PINK: [1, 2, 4],
    PropertyColor.BLACK: [1, 2, 3, 4],
    PropertyColor.RED: [2, 3, 6],
    PropertyColor.LIGHT_GREEN: [1, 2],
    PropertyColor.YELLOW: [2, 4, 6],
}

HOW_MANY_TO_COMPLETE = {
    PropertyColor.BROWN: 2,
    PropertyColor.DARK_BLUE: 2,
    PropertyColor.GREEN: 3,
    PropertyColor.LIGHT_BLUE: 3,
    PropertyColor.ORANGE: 3,
    PropertyColor.PINK: 3,
    PropertyColor.BLACK: 4,
    PropertyColor.RED: 3,
    PropertyColor.LIGHT_GREEN: 2,
    PropertyColor.YELLOW: 3,
}


class PropertySet:
    def __init__(self, colors: List[PropertyColor]):
        self.id = uuid.uuid4()
        self.properties = []
        self.colors = colors
        self.hasHouse = False
        self.hasHotel = False

    def add_property(self, property):
        if not self.can_add_property(property):
            return

        self.properties.append(property)
        self.colors = list(set(self.colors).intersection(property.colors))

    def can_add_property(self, property):
        if self.is_completed():
            return False

        my_colors = set(self.colors)
        other_colors = set(property.colors)
        has_common_color = len(my_colors.intersection(other_colors)) > 0
        at_least_one_non_wild = self.number_of_properties() == 0 or (
            len(self.colors) == 1 or len(property.colors) == 1
        )
        return has_common_color and at_least_one_non_wild

    def remove_property(self, property):
        # TODO: MAKE THIS WORK WITH "self.properties.remove(property)"
        for p in self.properties:
            if p.id == property.id:
                self.properties.remove(p)
                break

    def has_property(self, property):
        # TODO: MAKE THIS WORK WITH "property in self.properties"
        for p in self.properties:
            if p.id == property.id:
                return True
        return False

    def number_of_properties(self):
        return len(self.properties)

    # Returns the value of the current property set that will be used
    # as the rent value
    def rent_value(self):
        rent = 0
        if self.is_color_defined():
            n_properties = len(self.properties)
            property_color = self.colors[0]
            rent = RENT_VALUE[property_color][n_properties - 1]

        if self.hasHouse:
            rent += 3

        if self.hasHotel:
            rent += 4

        return rent

    # Returns the number of properties that this property set needs for it to be completed
    def number_to_complete(self):
        if self.is_color_defined():
            return HOW_MANY_TO_COMPLETE[self.colors[0]]

        # If there's only a multi color property, we will assume the maximum number it needs
        # based on the colors available on this multi color property
        p = [PropertySet([x]) for x in self.colors]
        return max([x.number_to_complete() for x in p])

    def add_house(self):
        if not self.can_add_house():
            print("Couldn't add house")
            return

        self.hasHouse = True

    def add_hotel(self):
        if not self.hasHouse:
            print("Tried to add Hotel in non House set")
            return

        self.hasHotel = True

    def is_completed(self):
        return (
            self.is_color_defined()
            and self.number_of_properties() >= self.number_to_complete()
        )

    def is_color_defined(self):
        return len(self.colors) == 1 and self.colors[0] != PropertyColor.RAINBOW

    def is_utility(self):
        return (
            self.colors[0] == PropertyColor.BLACK
            or self.colors[0] == PropertyColor.LIGHT_GREEN
        )

    def can_add_house(self):
        return self.is_completed() and self.is_color_defined() and not self.is_utility()

    def __repr__(self):
        return str(self.properties)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)
