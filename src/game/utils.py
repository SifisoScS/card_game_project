def calculate_score(hand):
    return sum(card.rank for card in hand)
