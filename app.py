from flask import Flask, render_template, request, redirect, url_for
from game_logic.game import determine_winners
from game_logic.player import Player
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        players = []
        
        # Process each player
        for i in range(1, 5):  # Up to 4 players
            name = request.form.get(f'player{i}_name')
            if not name and i > 2:  # Players 3 and 4 are optional
                continue
            
            # Collect all 5 cards for this player
            cards = []
            for card_num in range(5):
                card = request.form.get(f'player{i}_card{card_num}')
                if card:
                    cards.append(card.upper())
            
            if len(cards) != 5:
                flash(f'Player {i} must have exactly 5 cards', 'error')
                return redirect(url_for('play'))
            
            players.append(Player(name.strip(), cards))
        
        if len(players) < 2:
            flash('At least 2 players are required', 'error')
            return redirect(url_for('play'))
        
        # Check for duplicate cards
        all_cards = [card for player in players for card in player.cards]
        if len(all_cards) != len(set(all_cards)):
            flash('Each card must be unique across all players', 'error')
            return redirect(url_for('play'))
        
        winners = determine_winners(players)
        return render_template('results.html', players=players, winners=winners)
    
    return render_template('play.html')

if __name__ == '__main__':
    app.run(debug=True)