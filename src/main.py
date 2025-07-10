from game.deck import Deck
from game.player import Player
from game.game_logic import GameLogic
from interface.cli import CLI

def main():
    cli = CLI()
    cli.start_game()

if __name__ == "__main__":
    main()
