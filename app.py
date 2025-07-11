from flask import Flask, render_template, request, redirect, url_for, flash, session
from game_logic.game import Game
from game_logic.player import Player
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        players = []

        # Process player names
        for i in range(1, 5):  # Up to 4 players
            name = request.form.get(f'player{i}_name')
            if not name:
                if i > 2:
                    continue
                flash(f'Player {i} name is required', 'error')
                return redirect(url_for('play'))
            players.append(name.strip())

        if len(players) < 2:
            flash('At least 2 players are required', 'error')
            return redirect(url_for('play'))

        try:
            # Create a new Game instance per request
            game = Game()
            game_players = game.deal_cards(players, cards_per_player=3)

            # Check for duplicate cards
            all_cards = [card for player in game_players for card in player.cards]
            if len(all_cards) != len(set(all_cards)):
                flash('Each card must be unique across all players', 'error')
                return redirect(url_for('play'))

            # Store game state in session
            session['game_state'] = {
                'players': [
                    {'name': player.name, 'cards': player.cards, 'score': player.score, 'suit_score': player.suit_score}
                    for player in game_players
                ],
                'round_number': game.round_number
            }

            # Determine winners
            winners = game.determine_winners()
            return render_template('results.html', players=game_players, winners=winners)

        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('play'))

    return render_template('play.html')

if __name__ == '__main__':
    app.run(debug=True)