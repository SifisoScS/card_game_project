import unittest
from game.card import Card

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card('Hearts', 10)
        self.assertEqual(str(card), '10 of Hearts')