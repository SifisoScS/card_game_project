import unittest
from game_logic.game import determine_winners
from game_logic.player import Player

class TestGame(unittest.TestCase):
    def test_determine_winners(self):
        player1 = Player("Alice", ["AH", "KH", "QH", "JH", "10H"])
        player2 = Player("Bob", ["AC", "KC", "QC", "JC", "10C"])
        
        winners = determine_winners([player1, player2])
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0].name, "Alice")
    
    def test_tie_breaker(self):
        player1 = Player("Alice", ["AH", "KH", "QH", "JH", "10H"])
        player2 = Player("Bob", ["AS", "KS", "QS", "JS", "10S"])
        
        winners = determine_winners([player1, player2])
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0].name, "Bob")  # Higher suit score
    
    def test_multiple_winners(self):
        player1 = Player("Alice", ["AH", "KH", "QH", "JH", "10H"])
        player2 = Player("Bob", ["AH", "KH", "QH", "JH", "10H"])
        
        winners = determine_winners([player1, player2])
        self.assertEqual(len(winners), 2)

if __name__ == '__main__':
    unittest.main()