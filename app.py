from flask import Flask, render_template, request, redirect, url_for, flash
from game_logic.game import Game
from game_logic.player import Player
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

game = Game()  # Initialize Game instance to manage deck and state

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
            if not name and i > 2:  # Players 3 and 4 are optional
                continue
            if not name:
                flash(f'Player {i} name is required', 'error')
                return redirect(url_for('play'))
            players.append(name.strip())
        
        if len(players) < 2:
            flash('At least 2 players are required', 'error')
            return redirect(url_for('play'))
        
        try:
            # Deal cards to players using Game class
            game.reset_round()  # Reset for a new round
            game_players = game.deal_cards(players, cards_per_player=3)
            
            # Check for duplicate cards
            all_cards = [card for player in game_players for card in player.cards]
            if len(all_cards) != len(set(all_cards)):
                flash('Each card must be unique across all players', 'error')
                return redirect(url_for('play'))
            
            # Determine winners
            winners = game.determine_winners()
            return render_template('results.html', players=game_players, winners=winners)
        
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('play'))
    
    return render_template('play.html')

if __name__ == '__main__':
    app.run(debug=True)