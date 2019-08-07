from card import *

# Array where all the cards of the deck will be stored
ALL_CARDS = []

# ============================= MONEY ============================= #

# Creates the correct 'MoneyCard' object based on the 'n' passed to
# this function and gives each one a flag (first argument of the constructor)
def getMoney(n):
  if n == 1:
    return MoneyCard(5, "1M", 1)
  elif n == 2:
    return MoneyCard(4, "2M", 2)
  elif n == 3:
    return MoneyCard(3, "3M", 3)
  elif n == 4:
    return MoneyCard(2, "4M", 4)
  elif n == 5:
    return MoneyCard(1, "5M", 5)
  elif n == 10:
    return MoneyCard(0, "10M", 10)

# Adds the correct amount of each money bill in the game
for i in range(1):
  ALL_CARDS.append(getMoney(10))

for i in range(2):
  ALL_CARDS.append(getMoney(5))

for i in range(3):
  ALL_CARDS.append(getMoney(4))

for i in range(3):
  ALL_CARDS.append(getMoney(3))

for i in range(5):
  ALL_CARDS.append(getMoney(2))

for i in range(6):
  ALL_CARDS.append(getMoney(1))



# ============================= PROPERTY ============================= #

# Adds the correct amount of each property card in the game and gives each one
# a flag number (first argument of the constructor)
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



# ============================= RENT ============================= #

# Adds the correct amount of each rent card in the game and gives each one
# a flag number (first argument of the constructor)
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



# ============================= ACTIONS ============================= #

# Defines flags for each of the action cards. This is useful in other parts
# of the code as well.
DEAL_BREAKER = 30
DEBT_COLLECTOR = 31
DOUBLE_RENT = 32
FORCED_DEAL = 33
HOTEL = 34
HOUSE = 35
ITS_MY_BIRTHDAY = 36
JUST_SAY_NO = 37
PASS_GO = 38
SLY_DEAL = 39

# Adds the correct amount of each action card in the game and gives each one
# a flag number (first argument of the constructor)
for i in range(2):
  ALL_CARDS.append(ActionCard(DEAL_BREAKER, "Deal Braker", 5, "Steal a completed set"))

for i in range(3):
  ALL_CARDS.append(ActionCard(DEBT_COLLECTOR, "Debt Collector", 3, "Force someone to give you 5M"))

for i in range(2):
  ALL_CARDS.append(ActionCard(DOUBLE_RENT, "Double the Rent", 1, "Double the rent"))

for i in range(4):
  ALL_CARDS.append(ActionCard(FORCED_DEAL, "Forced Deal", 3, "Swap any non completed property"))

for i in range(3):
  ALL_CARDS.append(ActionCard(HOTEL, "Hotel", 4, "Add on top of a house"))

for i in range(3):
  ALL_CARDS.append(ActionCard(HOUSE, "House", 3, "Add on top of a completed set"))

for i in range(3):
  ALL_CARDS.append(ActionCard(ITS_MY_BIRTHDAY, "It's my birthday", 2, "Get 2M from everyone"))

for i in range(3):
  ALL_CARDS.append(ActionCard(JUST_SAY_NO, "Just Say No", 4, "No"))

for i in range(10):
  ALL_CARDS.append(ActionCard(PASS_GO, "Pass Go", 1, "Draw 2"))

for i in range(3):
  ALL_CARDS.append(ActionCard(SLY_DEAL, "Sly Deal", 3, "Steal a non pSet property"))