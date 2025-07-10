def determine_winners(players):
    if not players:
        return []
    
    max_score = max(player.score for player in players)
    potential_winners = [player for player in players if player.score == max_score]
    
    if len(potential_winners) > 1:
        max_suit_score = max(player.suit_score for player in potential_winners)
        potential_winners = [player for player in potential_winners if player.suit_score == max_suit_score]
    
    return potential_winners