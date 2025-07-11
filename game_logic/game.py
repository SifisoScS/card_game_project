import random
from .player import Player

class Game:
    def __init__(self):
        self.deck = self.create_deck()
        self.players = []
        self.round_number = 0

    def create_deck(self):
        """Create a standard 52-card deck."""
        suits = ['C', 'D', 'H', 'S']
        faces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [(face, suit) for suit in suits for face in faces]

    def shuffle_deck(self):
        """Shuffle the deck to randomize card order."""
        random.shuffle(self.deck)

    def deal_cards(self, players, cards_per_player=3):
        """Deal a specified number of cards to each player."""
        if not self.deck:
            self.deck = self.create_deck()
            self.shuffle_deck()
        
        if len(self.deck) < len(players) * cards_per_player:
            raise ValueError("Not enough cards in the deck to deal.")
        
        self.players = [Player(name, []) for name in players]
        for _ in range(cards_per_player):
            for player in self.players:
                if self.deck:
                    card = self.deck.pop(0)
                    player.cards.append(card)
                    player.calculate_score()
        
        self.round_number += 1
        return self.players

    def determine_winners(self):
        """Determine the winner(s) based on scores and suit scores."""
        if not self.players:
            return []
        
        try:
            max_score = max(player.score for player in self.players)
            potential_winners = [player for player in self.players if player.score == max_score]
            
            if len(potential_winners) > 1:
                max_suit_score = max(player.suit_score for player in potential_winners)
                potential_winners = [player for player in potential_winners if player.suit_score == max_suit_score]
            
            return potential_winners
        except ValueError as e:
            print(f"Error determining winners: {e}")
            return []

    def reset_round(self):
        """Reset the game for a new round, keeping players but clearing cards."""
        for player in self.players:
            player.cards = []
            player.score = 0
            player.suit_score = 0
        self.deck = self.create_deck()
        self.shuffle_deck()