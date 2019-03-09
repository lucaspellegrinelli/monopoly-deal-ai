class AI:

  # ------------------------------ Function Role ------------------------------
  #
  # Choose what function the player will take next
  #
  # ----------------------- You'll need these functions -----------------------
  #
  # - Game.applyAction(Action): void
  # --- Apply the action's effect into that instance of the game
  #
  # - Game.getTurnPossibleMoves(Player): void
  # --- Returns a list of all possible actions the specified player can do
  #
  # ----------------------------- Inputs/Outputs -----------------------------
  #
  # - INPUTS
  # --- instance: Game
  # ------ The instance of the game
  # --- player: Player
  # ------ A copy of the player object
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
  def chooseMove(self, instance, player, moves_left):
    raise NotImplementedError("Please implement the method 'chooseMove' in the subclass")

  # ------------------------------ Function Role ------------------------------
  #
  # Choose with what cards the player will pay a certain payment
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
  # --- player: Player
  # ------ A copy of the player object
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
  def choosePayment(self, instance, player, how_much):
    raise NotImplementedError("Please implement the method 'choosePayment' in the subclass")

  # ------------------------------ Function Role ------------------------------
  #
  # Choose what you'll discard after ending your turn with more than 7 cards.
  # You need to end up with 7 cards in hand.
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
  # --- player: Player
  # ------ A copy of A copy of the player object
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
  def chooseWhatToDiscard(self, instance, player):
    raise NotImplementedError("Please implement the method 'chooseWhatToDiscard' in the subclass")

  # ------------------------------ Function Role ------------------------------
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
  # --- player: Player
  # ------ A copy of the player object
  # --- properties: list of PropertyCard
  # ------ The properties you recieved as payment (other cards are already
  #        processed)
  #
  # - OUTPUT
  # --- N/A
  #
  # ------------------------------- Observations -------------------------------
  #
  # - If you don't address all the cards, the method will be called again but
  # only with the remaining cards to be addressed. The method will be re-called
  # WITH THE SAME INSTANCE AS BEFORE.
  #
  # - If there aren't any actions returned, an exception will be raised.
  #
  # ---------------------------------------------------------------------------
  def recievePayment(self, instance, player, properties):
    raise NotImplementedError("Please implement the method 'recievePayment' in the subclass")

  # ------------------------------ Function Role ------------------------------
  #
  # Deciding whether or not you'll negate the effect of a card thrown at you
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
  # --- player: Player
  # ------ A copy of the player object
  #
  # - OUTPUT
  # --- will_negate: boolean
  # ------ The decision of you'll negate or not
  #
  # ------------------------------- Observations -------------------------------
  #
  # If the return value is not a boolean, an exception will be raised
  #
  # ---------------------------------------------------------------------------
  def willNegate(self, instance, player):
    raise NotImplementedError("Please implement the method 'willNegate' in the subclass")
