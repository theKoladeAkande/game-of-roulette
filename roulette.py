class Outcome:
    
    """ Contains a single outcome on which 
    a bet can be placed"""

    def __init__(self, name: str, odds: int):
        self.name = name
        self.odds = odds
            
    def __eq__(self, other):
        if isinstance(other, Outcome):
            return other.name == self.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
            
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return f'{self.name} {self.odds}:1'
    
    def __repr__(self):
        return f"Outcome(name='{self.name}', odds={self.odds})"
        
        
    def win_amount(self, amount):
        """Calculates the win amount for the odds """
        return self.odds * amount


class Bin(frozenset):
    
    """contains a collection of Outcome instances which
    reflect the winning bets that are paid for a particular
    bin on a Roulette wheel"""
    pass