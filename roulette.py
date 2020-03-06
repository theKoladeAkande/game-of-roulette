import os
from random import Random
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

class Wheel: 
    def __init__(self):

        self.bins = tuple(Bin for _ in range(38))
        self.randgenerator = Random()
    
    def add_outcome(self, number, outcome):

        temp_bins = [*self.bins]
        temp_bins[number] = temp_bins[number](outcome)
        self.bins = tuple(temp_bins)

        
    def choose(self):
        """ use random generator to simulate wheel spining"""
        return self.randgenerator.choice(self.bins)
        
    def get(self, bin_num):
        return  self.bins[bin_num]


class BinBuilder:
    """Builds bin instances for various outcomes"""
    def __init__(self):
        pass
    
    def build_straight_bet(self, wheel: Wheel, outcome: Outcome):
        """Generates straight bets for individual bins"""
        wheel = wheel()
        
        for n in range(0,38):
            if n == 37:
                outcome = outcome('00', 35)
                wheel.add_outcome(n, {outcome})
            else:
                outcome = outcome(f'{n}', 35)
                wheel.add_outcome(n,{outcome})


    def build_split_bet(self, wheel: Wheel, outcome: Outcome):
        """Generates split bet for bins"""
        bins_set = {i:set() for i in range(1,37)}
        wheel = wheel()

        for row in range(12):
            #get elements in first column
            n_column_1 = 3*row + 1
            #split bet on column 1-2
            split_left = {n_column_1, n_column_1+1}
            outcome_1 = outcome(f'{split_left}', 17)
            #add outcome objects to sets
            bins_set[n_column_1].add(outcome_1)
            bins_set[n_column_1+1].add(outcome_1)

            #get elements for  column 2
            n_column_2 = 3*row + 2
            #split bets for column 2-3
            split_right = {n_column_2, n_column_2+1}
            outcome_2 = outcome(f'{split_right}', 17)
            bins_set[n_column_2].add(outcome_2)
            bins_set[n_column_2+1].add(outcome_2)

        for n in range(1, 33):
            #create up-down splitbet
            split_updown = {n, n+3}
            outcome = outcome(f'{split_updown}', 17)
            #add out outcome objects to set
            bins_set[n].add(outcome)
            bins_set[n+3].add(outcome)

        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])


    def build_street_bet(self, wheel: Wheel, outcome: Outcome):
        """Generate street for individual bins"""
        bins_set = {i:set() for i in range(1,37)}
        wheel = wheel()

        for row in range(12):
            n = 3*row + 1
            street = {n, n+1, n+2}
            outcome = outcome(f'{street}street', 11)
            bins_set[n].add(outcome)
            bins_set[n+1].add(outcome)
            bins_set[n+2].add(outcome)
        
        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])
    
    def build_corner_bets(self, wheel: Wheel, outcome: Outcome):
        """Generates corner bets"""
        bins_set = {i:set() for i in range(1,37)}
        wheel = wheel()

        for row in range(11):
            n_1_2 = 3*row + 1
            corner_1_2 = {n_1_2, n_1_2+1, n_1_2+3, n_1_2+4}
            outcome_1_2 = outcome(f'{corner_1_2}corner', 8)
            
            for  i in corner_1_2:
                bins_set[i].add(outcome_1_2)
        
            n_2_3 = 3*row + 2
            corner_2_3 = {n_2_3, n_2_3+1, n_2_3+3, n_2_3+4}
            outcome_2_3 = outcome(f'{corner_2_3}corner', 8)

            for i in corner_2_3:
                bins_set[i].add(outcome_2_3)
        
        for i in range(1, 37):
            wheel.add_outcome(i, bins_set[i])


    def build_line_bets(self, wheel: Wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
        wheel = wheel()
            
        for row in range(11):
            n = 3*row + 1
            line_bet = {n, n+1, n+2, n+3, n+4, n+5}
            outcome = outcome(f'{line_bet}line', 5)
            for i in line_bet:
                bins_set[i].add(outcome)
        
        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])
    

    def build_dozen_bets(self, wheel: wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
        wheel = wheel()
        for n in range(3):
            n_dozen = n + 1
            outcome = outcome(f'{n_dozen}dozen', 2)
            for i in range(12):
                bin_num = 12*n + i + 1
                bins_set[i].add(bin_num, outcome)
        
        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])


    def build_column_bets(self, wheel: Wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
        wheel = wheel()
            
        for n in range(3):
            column = n+1
            outcome = outcome(f'{column}column', 2)
            
            for i in range(12):
                rows = 3*i + n + 1
                bins_set[rows].add(outcome)
        
        for i in range(1, 37):
            wheel.add_outcome(i, bins_set[i])


    def build_even_money_bets(self, wheel: Wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
        wheel = wheel()
        outcome_red = outcome('Red', 1)
        outcome_black = outcome('Black', 1)
        outcome_even = outcome('Even', 1)
        outcome_odd = outcome('Odd', 1)
        outcome_high = outcome('High', 1)
        outcome_low = outcome('Low', 1)
        RED = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        
        for i in range(1, 37):
            if i < 19:
                bins_set[i].add(outcome_low)
            if i > 18:
                bins_set[i].add(outcome_high)
            if i % 2 == 0:
                bins_set[i].add(outcome_even)
            if i % 2 != 0:
                bins_set[i].add(outcome_odd)
            if i in  RED:
                bins_set[i].add(outcome_red)
            if i not in RED:
                bins_set[i].add(outcome_black)
        
        for i in range(1, 37):
            wheel.add_outcome(i, bins_set[i])


    def build_five_bet(self, wheel: Wheel, outcome: Outcome):
        five_bins = {0, 37, 1, 2, 3}
        five = outcome("00-0-1-2-3", 6)
        wheel = wheel()
        
        for n in five_bins:
            wheel.add_outcome(n, five)
                
