# - Abstract class of an Artificial Intellience
class AI:

  # ------------------------------- Method Role -------------------------------
  #
  # Choose what action the player will take next
  #
  # ----------------------- You'll need these functions -----------------------
  #
  # - Game.applyAction(Action): void
  # --- Apply the action's effect into that instance of the game
  #
  # - Game.getInstance(Player): Game
  # --- Get the instance of the game from the perspective of one player (the
  #     only player where the cards in hand are accurate with the real game
  #     is the specified player)
  #
  # - Game.getTurnPossibleMoves(Player): void
  # --- Returns a list of all possible actions the specified player can do
  #
  # ----------------------------- Inputs/Outputs -----------------------------
  #
  # - INPUTS
  # --- instance: Game
  # ------ The instance of the game
  # --- player_id: integer
  # ------ The id of the player
  # --- moves_left: integer
  # ------ How many moves left the player still has in his turn
  #
  # - OUTPUT
  # --- action: Action
  # ------ The action chosen for the player to take
  #
  # ------------------------------- Observations -------------------------------
  #
  # - If this method doesn't return a valid action, "DoNothingAction" will be
  # the replacement.
  #
  # ---------------------------------------------------------------------------
  def chooseMove(self, instance, player_id, moves_left):
    raise NotImplementedError("Please implement the method 'chooseMove' in the subclass")

  # ------------------------------- Method Role -------------------------------
  #
  # Choose with what cards the player will pay a certain payment
  #
  # ----------------------- You'll need these functions -----------------------
  #
  # - Read "property_set.py" for all methods about the PropertySet class
  # - Read "card.py" for all methods about the PropertyCard class
  #
  # ----------------------------- Inputs/Outputs -----------------------------
  #
  # - INPUTS
  # --- instance: Game
  # ------ The instance of the game
  # --- player_id: integer
  # ------ The id of the player
  # --- player_sets: list of PropertySet
  # ------ All the properties the player controls
  # --- player_money_pile: list of Card
  # ------ All cards in the player money pile
  # --- how_much: integer
  # ------ How many "money" you need to pay
  #
  # - OUTPUT
  # --- payment: list of Card
  # ------ The cards chosen for the payment
  #
  # ------------------------------- Observations -------------------------------
  #
  # - This method will be called in a loop until the payment is enough or the
  # player doesn't have anymore cards. The method will be re-called
  # WITH THE SAME INSTANCE AS BEFORE.
  #
  # - If no cards are returned, an exception will be raised
  #
  # ---------------------------------------------------------------------------
  def choosePayment(self, instance, player_id, player_sets, player_money_pile, how_much):
    raise NotImplementedError("Please implement the method 'choosePayment' in the subclass")

  # ------------------------------- Method Role -------------------------------
  #
  # Choose what you'll discard after ending your turn with more than 7 cards.
  # You need to end up with 7 cards in hand.
  #
  # ----------------------- You'll need these functions -----------------------
  #
  # - Read "card.py" for all methods about all the different Card subclasses
  #
  # ----------------------------- Inputs/Outputs -----------------------------
  #
  # - INPUTS
  # --- instance: Game
  # ------ The instance of the game
  # --- player_id: integer
  # ------ The id of the player
  # --- player_hand: list of Card
  # ------ All the cards in the player hand
  #
  # - OUTPUT
  # --- cards: list of Card
  # ------ The cards you'll discard
  #
  # ------------------------------- Observations -------------------------------
  #
  # - If you don't discard enough cards, this will be called again until the
  # number of cards discarded is enough. The method will be re-called
  # WITH THE SAME INSTANCE AS BEFORE.
  #
  # - If this doesn't return any cards, an exception will be raised
  #
  # ---------------------------------------------------------------------------
  def chooseWhatToDiscard(self, instance, player_id, player_hand):
    raise NotImplementedError("Please implement the method 'chooseWhatToDiscard' in the subclass")

  # ------------------------------- Method Role -------------------------------
  #
  # Add the new properties to currently existing sets or create new sets to add
  # them.
  #
  # ----------------------- You'll need these functions -----------------------
  #
  # - PropertySet(colors: list of integers): PropertySet
  # --- Constructor of a new set. Check the color flags in the "cardconsts.py"
  #     file
  #
  # - PropertySet.canAddProperty(PropertyCard): boolean
  # --- Checks if you can add the specified property into that set and returns
  #     True or False for that
  #
  # - PropertySet.addProperty(PropertyCard): void
  # --- Checks if you can add the specified property into that set and if you
  #     can, add it. Doesn't return anything
  #
  # - Player.addPropertySet(PropertySet): void
  # --- Adds the specified property set to the player current field
  #
  # ----------------------------- Inputs/Outputs -----------------------------
  #
  # - INPUTS
  # --- instance: Game
  # ------ The instance of the game
  # --- player_id: integer
  # ------ The id of the player
  # --- properties: list of PropertyCard
  # ------ The properties you recieved as payment (other cards are already
  #        processed)
  #
  # - OUTPUT
  # --- actions: list of PlayPropertyAction
  # ------ All the actions like "put this property in the set" using actions
  #        like PlayPropertyAction
  #
  # ------------------------------- Observations -------------------------------
  #
  # - If you don't address all the cards, the method will be called again but
  # only with the remaining cards to be addressed. The method will be re-called
  # WITH THE SAME INSTANCE AS BEFORE.
  #
  # - If there aren't any actions returned, an exception will be raised.
  #
  # - If any of the actions returned are not PlayPropertyAction, an exception will
  # be raised
  #
  # - If you try to play a property you didn't recieve, an exception will be
  # raised
  #
  # ---------------------------------------------------------------------------
  def recievePropertiesFromPayment(self, instance, player_id, properties):
    raise NotImplementedError("Please implement the method 'recievePayment' in the subclass")

  # ------------------------------- Method Role -------------------------------
  #
  # Deciding whether or not you'll negate the effect of a card thrown at you
  #
  # ----------------------- You'll need these functions -----------------------
  #
  # - Action.who_used: Player
  # --- The copy of the player that used that card
  #
  # - isinstance(action, StealPropertyAction)
  # --- Test if its a Sly Deal card
  # --- See more attributes of this action in action.py
  #
  # - isinstance(action, StealPropertySetAction)
  # --- Test if its a Deal Breaker card
  # --- See more attributes of this action in action.py
  #
  # - isinstance(action, SwapPropertyAction)
  # --- Test if its a Froced Deal card
  # --- See more attributes of this action in action.py
  #
  # - isinstance(action, AskMoneyAction)
  # --- Test if its an action that gets money from you (rent, birthday, ...)
  # --- See more attributes of this action in action.py
  #
  # ----------------------------- Inputs/Outputs -----------------------------
  #
  # - INPUTS
  # --- instance: Game
  # ------ The instance of the game
  # --- player_id: integer
  # ------ The id of the player
  # --- action: Action
  # ------ The action to negate (or not)
  #
  # - OUTPUT
  # --- will_negate: boolean
  # ------ The decision of you'll negate or not
  #
  # ------------------------------- Observations -------------------------------
  #
  # - If the return value is not a boolean, an exception will be raised
  #
  # ---------------------------------------------------------------------------
  def willNegate(self, instance, player_id, action):
    raise NotImplementedError("Please implement the method 'willNegate' in the subclass")

  # ------------------------------- Method Role -------------------------------
  #
  # Arrange your cards so they fit better the player interest reagarding
  # their placements on the sets
  #
  # ----------------------- You'll need these functions -----------------------
  #
  # - N/A
  #
  # ----------------------------- Inputs/Outputs -----------------------------
  #
  # - INPUTS
  # --- instance: Game
  # ------ The instance of the game
  # --- player_id: integer
  # ------ The id of the player
  # --- player_sets: list of PropertySet
  # ------ All the properties the player controls
  #
  # - OUTPUT
  # --- actions: list of MovePropertyAction
  # ------ The changes you'll be making to the arrangement of the wild cards
  #        in your field
  #
  # ------------------------------- Observations -------------------------------
  #
  # - This will be called right before the turn ends
  #
  # - If any of the actions returned are not MovePropertyAction, an exception will
  # be raised
  #
  # ---------------------------------------------------------------------------
  def rearrangeCards(self, instance, player_id, player_sets):
    raise NotImplementedError("Please implement the method 'rearrangeCards' in the subclass")
