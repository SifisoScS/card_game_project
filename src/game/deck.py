from .card import Card
import random

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                      for rank in range(1, 14)]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None
