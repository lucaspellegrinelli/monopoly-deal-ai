import card

ALL_CARDS = []

# ----------- MONEY ------------- #
for i in range(1):
  ALL_CARDS.append(MoneyCard(0, "10M", 10))

for i in range(2):
  ALL_CARDS.append(MoneyCard(1, "5M", 10))

for i in range(3):
  ALL_CARDS.append(MoneyCard(2, "4M", 4))

for i in range(3):
  ALL_CARDS.append(MoneyCard(3, "3M", 3))

for i in range(5):
  ALL_CARDS.append(MoneyCard(4, "2M", 2))

for i in range(6):
  ALL_CARDS.append(MoneyCard(5, "1M", 1))

# ----------- PROPERTY ------------- #
for i in range(2):
  ALL_CARDS.append(PropertyCard(6, "Brown Property", 1, [BROWN_PROPERTY]))

for i in range(2):
  ALL_CARDS.append(PropertyCard(7, "Dark Blue Property", 4, [DARK_BLUE_PROPERTY]))

for i in range(2):
  ALL_CARDS.append(PropertyCard(8, "Light Green Property", 2, [LIGHT_GREEN_PROPERTY]))

for i in range(3):
  ALL_CARDS.append(PropertyCard(9, "Green Property", 4, [GREEN_PROPERTY]))

for i in range(3):
  ALL_CARDS.append(PropertyCard(10, "Light Blue Property", 1, [LIGHT_BLUE_PROPERTY]))

for i in range(3):
  ALL_CARDS.append(PropertyCard(11, "Orange Property", 2, [ORANGE_PROPERTY]))

for i in range(3):
  ALL_CARDS.append(PropertyCard(12, "Pink Property", 2, [PINK_PROPERTY]))

for i in range(3):
  ALL_CARDS.append(PropertyCard(13, "Red Property", 3, [RED_PROPERTY]))

for i in range(3):
  ALL_CARDS.append(PropertyCard(14, "Yellow Property", 3, [YELLOW_PROPERTY]))

for i in range(4):
  ALL_CARDS.append(PropertyCard(15, "Black Property", 2, [BLACK_PROPERTY]))

for i in range(1):
  ALL_CARDS.append(PropertyCard(16, "Dark Blue/Green Property", 4, [DARK_BLUE_PROPERTY, GREEN_PROPERTY]))

for i in range(1):
  ALL_CARDS.append(PropertyCard(17, "Light Blue/Brown Property", 1, [LIGHT_BLUE_PROPERTY, BROWN_PROPERTY]))

for i in range(1):
  ALL_CARDS.append(PropertyCard(18, "Black/Green Property", 4, [BLACK_PROPERTY, GREEN_PROPERTY]))

for i in range(1):
  ALL_CARDS.append(PropertyCard(19, "Light Blue/Black Property", 4, [BLACK_PROPERTY, LIGHT_BLUE_PROPERTY]))

for i in range(1):
  ALL_CARDS.append(PropertyCard(20, "Black/Light Green Property", 2, [BLACK_PROPERTY, LIGHT_GREEN_PROPERTY]))

for i in range(2):
  ALL_CARDS.append(PropertyCard(21, "Pink/Orange Property", 2, [PINK_PROPERTY, ORANGE_PROPERTY]))

for i in range(2):
  ALL_CARDS.append(PropertyCard(22, "Red/Yellow Property", 3, [RED_PROPERTY, YELLOW_PROPERTY]))

for i in range(2):
  ALL_CARDS.append(PropertyCard(23, "Rainbow Property", 0, [RAINBOW_PROPERTY]))

# ----------- RENT ------------- #
for i in range(2):
  ALL_CARDS.append(RentCard(24, "Dark Blue/Green Rent", 1, [GREEN_PROPERTY, DARK_BLUE_PROPERTY], False))

for i in range(2):
  ALL_CARDS.append(RentCard(25, "Brown/Light Blue Rent", 1, [BROWN_PROPERTY, LIGHT_BLUE_PROPERTY], False))

for i in range(2):
  ALL_CARDS.append(RentCard(26, "Pink/Orange Rent", 1, [PINK_PROPERTY, ORANGE_PROPERTY], False))

for i in range(2):
  ALL_CARDS.append(RentCard(27, "Black/Light Green Rent", 1, [BLACK_PROPERTY, LIGHT_GREEN_PROPERTY], False))

for i in range(2):
  ALL_CARDS.append(RentCard(28, "Red/Yellow Rent", 1, [RED_PROPERTY, YELLOW_PROPERTY], False))

for i in range(3):
  ALL_CARDS.append(RentCard(29, "Wild Rent", 1, [], True))

# ----------- ACTION ------------- #
# TODO, I NEED THE GAME INSTANCE TO DO THIS
for i in range(2):
  ALL_CARDS.append(ActionCard(30, "Deal Braker", 5, "Steal a completed set"))

for i in range(3):
  ALL_CARDS.append(ActionCard(31, "Debt Collector", 3, "Force someone to give you 5M"))

for i in range(2):
  ALL_CARDS.append(ActionCard(32, "Double the Rent", 1, "Double the rent"))

for i in range(3):
  ALL_CARDS.append(ActionCard(33, "Forced Deal", 3, "Swap any non completed property"))

for i in range(3):
  ALL_CARDS.append(ActionCard(34, "Hotel", 4, "Add on top of a house"))

for i in range(3):
  ALL_CARDS.append(ActionCard(35, "Hotel", 3, "Add on top of a completed set"))

for i in range(3):
  ALL_CARDS.append(ActionCard(36, "It's my birthday", 2, "Get 2M from everyone"))

for i in range(3):
  ALL_CARDS.append(ActionCard(37, "Just Say No", 4, "No"))

for i in range(10):
  ALL_CARDS.append(ActionCard(38, "Pass Go", 1, "Draw 2"))

for i in range(3):
  ALL_CARDS.append(ActionCard(39, "Sly Deal", 3, "Steal a non set property"))
