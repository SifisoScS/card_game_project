"""
game_logic.py - Core game mechanics and rule enforcement
Handles all game state, player turns, scoring, and win conditions
"""

import random
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Optional
from functools import total_ordering

class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()

class Rank(Enum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2

@total_ordering
@dataclass
class Card:
    suit: Suit
    rank: Rank
    
    def __str__(self):
        return f"{self.rank.name.title()} of {self.suit.name.title()}"
    
    def __eq__(self, other):
        return self.rank == other.rank
    
    def __lt__(self, other):
        return self.rank.value < other.rank.value

@dataclass
class Player:
    name: str
    hand: List[Card] = None
    score: int = 0
        
    def __post_init__(self):
        self.hand = [] if self.hand is None else self.hand
    
    def draw_card(self, deck: List[Card]):
        if deck:
            self.hand.append(deck.pop())
    
    def play_card(self, card_index: int) -> Card:
        return self.hand.pop(card_index)
    
    def calculate_hand_strength(self) -> int:
        """Calculate overall strength of current hand"""
        if not self.hand:
            return 0
        return sum(card.rank.value for card in self.hand)

class GamePhase(Enum):
    SETUP = auto()
    BETTING = auto()
    DRAWING = auto()
    SHOWDOWN = auto()
    GAME_OVER = auto()

class GameMode(Enum):
    HIGH_CARD = auto()
    FIVE_CARD_DRAW = auto()
    BLACKJACK = auto()
    WAR = auto()

class GameLogic:
    def __init__(self, player_names: List[str], game_mode: GameMode = GameMode.HIGH_CARD):
        self.players = [Player(name) for name in player_names]
        self.deck = self._initialize_deck()
        self.discard_pile = []
        self.current_phase = GamePhase.SETUP
        self.game_mode = game_mode
        self.pot = 0
        self.current_player_index = 0
        self.round_number = 1
        self.winner = None
        self.history = []
        self.max_rounds = 5  # Added max rounds to end the game
        
        # Game-specific settings
        self._set_mode_rules()
    
    def _set_mode_rules(self):
        """Configure rules based on selected game mode"""
        self.rules = {
            GameMode.HIGH_CARD: {
                'hand_size': 1,
                'scoring': self._score_high_card,
                'win_condition': self._check_high_card_win
            },
            GameMode.FIVE_CARD_DRAW: {
                'hand_size': 5,
                'scoring': self._score_poker_hand,
                'win_condition': self._check_poker_win
            }
        }.get(self.game_mode)
    
    def _initialize_deck(self) -> List[Card]:
        """Create and shuffle a standard 52-card deck"""
        deck = [Card(suit, rank) for suit in Suit for rank in Rank]
        random.shuffle(deck)
        return deck
    
    def start_game(self):
        """Begin the game proper"""
        self.current_phase = GamePhase.BETTING
        self._deal_initial_cards()
        self._record_state("Game started")
    
    def next_turn(self):
        """Progress to the next player's turn"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Check for round/game completion
        if self.current_player_index == 0:
            self._check_round_completion()
    
    def _deal_initial_cards(self):
        """Deal starting hands to all players"""
        hand_size = self.rules['hand_size']
        for _ in range(hand_size):
            for player in self.players:
                if not self.deck:
                    self._shuffle_discard_pile()
                player.draw_card(self.deck)
        self._record_state("Initial cards dealt")
    
    def _check_round_completion(self):
        """Evaluate end-of-round conditions"""
        if all(len(player.hand) == 0 for player in self.players):
            self.current_phase = GamePhase.SHOWDOWN
            self._determine_round_winner()
    
    def _determine_round_winner(self):
        """Calculate scores and determine the winning player"""
        for player in self.players:
            player.score += self.rules['scoring'](player)
        
        self.winner = self.rules['win_condition']()
        self._record_state(f"Round {self.round_number} winner: {self.winner}")
        
        # Check if game should end
        if self.round_number >= self.max_rounds or self.winner is not None:
            self.current_phase = GamePhase.GAME_OVER
        else:
            self.round_number += 1
            # Reset for next round
            self._prepare_next_round()
    
    def _prepare_next_round(self):
        """Reset game state for subsequent rounds"""
        self.discard_pile = []
        for player in self.players:
            player.hand.clear()
        
        if len(self.deck) < len(self.players) * self.rules['hand_size']:
            self._shuffle_discard_pile()
        
        self.current_phase = GamePhase.BETTING
        self._deal_initial_cards()
    
    def _shuffle_discard_pile(self):
        """Recycle discard pile into the deck"""
        self.deck.extend(self.discard_pile)
        self.discard_pile = []
        random.shuffle(self.deck)
        self._record_state("Shuffled discard pile into deck")
    
    def _score_high_card(self, player: Player) -> int:
        """Simple scoring based on highest card value"""
        if not player.hand:
            return 0
        return max(card.rank.value for card in player.hand)
    
    def _score_poker_hand(self, player: Player) -> int:
        """Calculate poker hand strength"""
        if len(player.hand) != 5:
            return 0
            
        # Simplified poker scoring (real implementation would be more complex)
        ranks = [card.rank.value for card in player.hand]
        suits = [card.suit for card in player.hand]
        
        # Check for flush
        if len(set(suits)) == 1:
            return sum(ranks) + 1000
            
        # Check for straight
        if all(ranks[i] == ranks[i+1]-1 for i in range(4)):
            return sum(ranks) + 800
            
        # Check for pairs/trips/etc.
        rank_counts = {r: ranks.count(r) for r in set(ranks)}
        if any(v == 4 for v in rank_counts.values()):  # Four of a kind
            return sum(ranks) + 700
        if sorted(rank_counts.values()) == [2, 3]:  # Full house
            return sum(ranks) + 600
        if 3 in rank_counts.values():  # Three of a kind
            return sum(ranks) + 300
        if list(rank_counts.values()).count(2) == 2:  # Two pairs
            return sum(ranks) + 200
        if 2 in rank_counts.values():  # One pair
            return sum(ranks) + 100
            
        return sum(ranks)
    
    def _check_high_card_win(self) -> Optional[Player]:
        """Determine winner in high card mode"""
        scores = {player: self._score_high_card(player) for player in self.players}
        max_score = max(scores.values())
        winners = [p for p, s in scores.items() if s == max_score]
        
        if len(winners) == 1:
            return winners[0]
        
        # Handle ties (in real game might want tiebreaker rules)
        return None
    
    def _check_poker_win(self) -> Optional[Player]:
        """Determine winner in poker mode"""
        scores = {player: self._score_poker_hand(player) for player in self.players}
        max_score = max(scores.values())
        winners = [p for p, s in scores.items() if s == max_score]
        
        if len(winners) == 1:
            return winners[0]
        return None
    
    def _record_state(self, action: str):
        """Record game state snapshot for history/replays"""
        snapshot = {
            'round': self.round_number,
            'phase': self.current_phase.name,
            'action': action,
            'players': {p.name: len(p.hand) for p in self.players},
            'deck_cards': len(self.deck),
            'discard_pile': len(self.discard_pile)
        }
        self.history.append(snapshot)
    
    def get_game_state(self) -> Dict:
        """Return current game state for API/UI consumption"""
        return {
            'phase': self.current_phase.name,
            'current_player': self.players[self.current_player_index].name,
            'players': [
                {
                    'name': p.name,
                    'hand_size': len(p.hand),
                    'score': p.score
                } for p in self.players
            ],
            'pot': self.pot,
            'winner': self.winner.name if self.winner else None,
            'history': self.history
        }

# Helper methods for poker hand evaluation (simplified)
def _is_flush(cards: List[Card]) -> bool:
    suits = [c.suit for c in cards]
    return len(set(suits)) == 1

def _is_straight(cards: List[Card]) -> bool:
    ranks = sorted([c.rank.value for c in cards])
    return all(ranks[i] == ranks[i+1]-1 for i in range(len(ranks)-1))
