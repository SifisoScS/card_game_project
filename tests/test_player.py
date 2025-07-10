import unittest
from game.player import Player

class TestPlayer(unittest.TestCase):
    def test_add_card(self):
        player = Player('Alice')
        player.add_card('Ace of Spades')
        self.assertEqual(len(player.hand), 1)