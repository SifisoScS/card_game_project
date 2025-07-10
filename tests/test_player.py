import unittest
from game_logic.player import Player

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player("Alice", ["AH", "2C", "3D", "4S", "5H"])
        self.assertEqual(player.name, "Alice")
        self.assertEqual(player.cards, ["AH", "2C", "3D", "4S", "5H"])
    
    def test_score_calculation(self):
        player = Player("Bob", ["AH", "KH", "QH", "JH", "10H"])
        self.assertEqual(player.score, 31)  # A + K + Q = 11 + 10 + 10
    
    def test_suit_score_calculation(self):
        player = Player("Charlie", ["AC", "KD", "QH", "JS", "10C"])
        self.assertEqual(player.suit_score, 10)  # 1 + 2 + 3 + 4 + 1
    
    def test_invalid_card(self):
        player = Player("Dave", ["XX", "2C", "3D", "4S", "5H"])
        self.assertEqual(player.score, 14)  # 0 + 2 + 3 + 4 + 5 (top 3: 5,4,3)

if __name__ == '__main__':
    unittest.main()