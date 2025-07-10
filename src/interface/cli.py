from game.player import Player
from game.game_logic import GameLogic, GamePhase


class CLI:
    def start_game(self):
        print("Welcome to the Card Game!")
        
        # Input validation for number of players
        while True:
            try:
                num_players = int(input("Enter number of players: "))
                if num_players < 1:
                    print("Please enter a number greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        players = []

        for _ in range(num_players):
            name = input("Enter player name: ")
            players.append(Player(name))

        # Start the game logic
        game_logic = GameLogic([player.name for player in players])
        game_logic.start_game()

        while game_logic.current_phase != GamePhase.GAME_OVER:
            print(f"\n--- Round {game_logic.round_number} ---")
            for player in game_logic.players:
                print(f"{player.name}'s turn:")
                player.draw_card(game_logic.deck)  # Each player draws a card
                print(f"{player.name} drew a {player.hand[-1]}")

                # Prompt player to play a card
                while True:
                    print(f"{player.name}'s hand:")
                    for idx, card in enumerate(player.hand):
                        print(f"{idx}: {card}")
                    try:
                        card_index = int(input(f"Select a card index to play (0-{len(player.hand)-1}): "))
                        if 0 <= card_index < len(player.hand):
                            played_card = player.play_card(card_index)
                            print(f"{player.name} played {played_card}")
                            break
                        else:
                            print("Invalid index. Please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")
                    except KeyboardInterrupt:
                        print("\nGame interrupted by user. Exiting...")
                        exit(0)

            game_logic.next_turn()  # Move to the next player's turn

            if game_logic.current_player_index == 0:  # Check if round is complete
                game_logic._check_round_completion()

        # Display the winner
        if game_logic.winner:
            print(f"\nThe winner is: {game_logic.winner.name}!")
        else:
            print("It's a tie!")
