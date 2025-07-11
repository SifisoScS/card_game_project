class Player:
    def __init__(self, name, cards=None):
        """Initialize a player with a name and optional list of cards."""
        self.name = name
        self.cards = cards if cards is not None else []
        self.score = 0
        self.suit_score = 0
        if self.cards:
            self.calculate_score()

    def calculate_score(self):
        """Calculate the player's score based on their top 3 cards and suit values."""
        if not self.cards:
            self.score = 0
            self.suit_score = 0
            return
        
        face_card_values = []
        self.suit_score = 0
        
        for card in self.cards:
            if not isinstance(card, tuple) or len(card) != 2:
                print(f"Invalid card format for player {self.name}: {card}")
                continue
                
            face_value, suit = card
            face_value_score = self.get_face_value_score(face_value)
            face_card_values.append(face_value_score)
            suit_value_score = self.get_suit_value_score(suit)
            self.suit_score += suit_value_score
        
        face_card_values.sort(reverse=True)
        self.score = sum(face_card_values[:3]) if len(face_card_values) >= 3 else sum(face_card_values)

    def get_face_value_score(self, face_value):
        """Return the score for a card's face value."""
        face_value = str(face_value).upper()
        if face_value == 'A':
            return 11
        elif face_value in ['J', 'Q', 'K']:
            return 10
        try:
            value = int(face_value)
            if 2 <= value <= 10:
                return value
            return 0
        except ValueError:
            print(f"Invalid face value for player {self.name}: {face_value}")
            return 0

    def get_suit_value_score(self, suit):
        """Return the score for a card's suit."""
        return {
            'C': 1,  # Clubs
            'D': 2,  # Diamonds
            'H': 3,  # Hearts
            'S': 4   # Spades
        }.get(suit.upper(), 0)

    def add_card(self, card):
        """Add a single card to the player's hand and recalculate score."""
        if isinstance(card, tuple) and len(card) == 2:
            self.cards.append(card)
            self.calculate_score()
        else:
            print(f"Cannot add invalid card to {self.name}'s hand: {card}")