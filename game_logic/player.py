class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.score = 0
        self.suit_score = 0
        self.calculate_score()
    
    def calculate_score(self):
        face_card_values = []
        self.suit_score = 0
        
        for card in self.cards:
            face_value = card[0]
            suit = card[1] if len(card) > 1 else ''
            
            face_value_score = self.get_face_value_score(face_value)
            face_card_values.append(face_value_score)
            
            suit_value_score = self.get_suit_value_score(suit)
            self.suit_score += suit_value_score
        
        face_card_values.sort(reverse=True)
        self.score = sum(face_card_values[:3])
    
    def get_face_value_score(self, face_value):
        if face_value == 'A':
            return 11
        elif face_value in ['J', 'Q', 'K']:
            return 10
        else:
            try:
                return int(face_value)
            except ValueError:
                return 0
    
    def get_suit_value_score(self, suit):
        return {
            'C': 1,
            'D': 2,
            'H': 3,
            'S': 4
        }.get(suit, 0)