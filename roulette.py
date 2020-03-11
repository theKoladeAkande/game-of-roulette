import os
from random import Random
from dataclasses import dataclass
import collections

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


class Bin(set):
    
    """contains a collection of Outcome instances which
    reflect the winning bets that are paid for a particular
    bin on a Roulette wheel"""
    pass

class Wheel: 
    def __init__(self):

        self.bins = tuple(Bin() for _ in range(38))
        self.randgenerator = Random()
        self.all_outcomes = {}
    
    def add_outcome(self, number, outcome):
        if isinstance(outcome, set):
            for _outcome in outcome:
                self.all_outcomes[_outcome.name] = _outcome
            self.bins[number].update(outcome)
        else:
            self.all_outcomes[outcome.name] = outcome
            self.bins[number].add(outcome)

        
    def choose(self):
        """ use random generator to simulate wheel spining"""
        return self.randgenerator.choice(self.bins)
        
    def get_bin(self, bin_num):
        return  self.bins[bin_num]
    
        
    def get_outcome(self, name: str):
        return self.all_outcomes[name]
        
        

class BinBuilder:
    """Builds bin instances for various outcomes"""
    def __init__(self):
        pass
    
    def build_straight_bet(self, wheel: Wheel, outcome: Outcome):
        """Generates straight bets for individual bins"""
        
        
        for n in range(0,38):
            if n == 37:
                outcome_straight = outcome('00', 35)
                wheel.add_outcome(n, outcome_straight)
            else:
                outcome_straight = outcome(f'{n}', 35)
                wheel.add_outcome(n,outcome_straight)


    def build_split_bet(self, wheel: Wheel, outcome: Outcome):
        """Generates split bet for bins"""
        bins_set = {i:set() for i in range(1,37)}
        

        for row in range(12):
            #get elements in first column
            n_column_1 = 3*row + 1
            #split bet on column 1-2
            split_left = [n_column_1, n_column_1+1]
            outcome_1 = outcome(f'{split_left[0]}-{split_left[1]}', 17)
            #add outcome objects to sets
            bins_set[n_column_1].add(outcome_1)
            bins_set[n_column_1+1].add(outcome_1)

            #get elements for  column 2
            n_column_2 = 3*row + 2
            #split bets for column 2-3
            split_right = [n_column_2, n_column_2+1]
            outcome_2 = outcome(f'{split_right[0]}-{split_right[1]}', 17)
            bins_set[n_column_2].add(outcome_2)
            bins_set[n_column_2+1].add(outcome_2)

        for n in range(1, 34):
            #create up-down splitbet
            split_updown = [n, n+3]
            outcome_splitupdown = outcome(f'{split_updown[0]}-{split_updown[1]}', 17)
            bins_set[n].add(outcome_splitupdown)
            bins_set[n+3].add(outcome_splitupdown)

        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])


    def build_street_bet(self, wheel: Wheel, outcome: Outcome):
        """Generate street for individual bins"""
        bins_set = {i:set() for i in range(1,37)}

        for row in range(12):
            n = 3*row + 1
            street = [n, n+1, n+2]
            outcome_street = outcome(f'{street[0]}-{street[1]}-{street[2]}',
                                      11)
            
            for strt in street:
                bins_set[strt].add(outcome_street)
        
        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])
    
    def build_corner_bets(self, wheel: Wheel, outcome: Outcome):
        """Generates corner bets"""
        bins_set = {i:set() for i in range(1,37)}

        for row in range(11):
            n_1_2 = 3*row + 1
            corner_1_2 = [n_1_2, n_1_2+1, n_1_2+3, n_1_2+4]
            outcome_1_2 = outcome(f'{corner_1_2[0]}-{corner_1_2[1]}-{corner_1_2[2]}-{corner_1_2[3]}', 
                                  8)
            
            for  i in corner_1_2:
                bins_set[i].add(outcome_1_2)
        
            n_2_3 = 3*row + 2
            corner_2_3 = [n_2_3, n_2_3+1, n_2_3+3, n_2_3+4]
            outcome_2_3 = outcome(f'{corner_2_3[0]}-{corner_2_3[1]}-{corner_2_3[2]}-{corner_2_3[3]}', 
                                  8)

            for i in corner_2_3:
                bins_set[i].add(outcome_2_3)
        
        for i in range(1, 37):
            wheel.add_outcome(i, bins_set[i])


    def build_line_bets(self, wheel: Wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
       
            
        for row in range(11):
            n = 3*row + 1
            line_bet = [n, n+1, n+2, n+3, n+4, n+5]
            outcome_line = outcome(
                f'{line_bet[0]}-{line_bet[1]}-{line_bet[2]}-{line_bet[3]}-{line_bet[4]}-{line_bet[5]}', 
                                   5)
            for i in line_bet:
                bins_set[i].add(outcome_line)
        
        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])
    

    def build_dozen_bets(self, wheel: Wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
       
        for n in range(3):
            n_dozen = n + 1
            outcome_dozen = outcome(f'{n_dozen}-dozen', 2)
            for i in range(12):
                bin_num = 12*n + i + 1
                bins_set[bin_num].add(outcome_dozen)
        
        for i in range(1,37):
            wheel.add_outcome(i, bins_set[i])


    def build_column_bets(self, wheel: Wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
            
        for n in range(3):
            column = n+1
            outcome_column = outcome(f'{column}-column', 2)
            
            for i in range(12):
                rows = 3*i + n + 1
                bins_set[rows].add(outcome_column)
        
        for i in range(1, 37):
            wheel.add_outcome(i, bins_set[i])


    def build_even_money_bets(self, wheel: Wheel, outcome: Outcome):
        bins_set = {i:set() for i in range(1,37)}
       
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
       
        
        for n in five_bins:
            wheel.add_outcome(n, five)


@dataclass
class Bet:
    """ Associates an amount and an Outcome"""
    amount: int
    outcome: Outcome
    
    
    def win_amount(self):
        return self.outcome.win_amount(self.amount)
    
    def lose_amount(self):
        return self.amount
    
    def __str__(self):
        str_outcome = str(self.outcome)
        return f'{self.amount} on {str_outcome}'
    

class InvalidBet(Exception):
    pass


class Table:
    """contains all the Bet instances created by a Player object"""
    def __init__(self, *bets):
        self.bets = [*bets]
        self.limit = None
        self.minimum = None
        self.index = 0

    
    def __iter__(self):
        return self
    
   
    def __next__(self):
        if self.index == len(self.bets):
            raise StopIteration
        else:
            item = self.bets[self.index]
            self.index += 1
            return item
            
        
    def __repr__(self):
        all_bets = [bet() for bet in self.bets]
        all_bets = tuple(all_bets)
        return f'Table{all_bets}'
    
    
    def __str__(self):
        if self.bets:
            all_bets =[str(bet) for bet in self.bets]
            return f'all current bets are {all_bets}'
        else:
            return 'No current bets'

    
    def place_bet(self, bet: Bet):
        if not isinstance(bet, Bet):
            raise TypeError(f'{bet} not instance of Bet')
        self.bets.append(bet)        
    
    def is_valid(self):
        all_bets_amount = [bet.amount for bet in self.bets]
        if sum(all_bets_amount) > self.limit: 
            raise InvalidBet(f'The total bet amount is greater than table limit {self.limit}')
        if any(map(lambda x: x < self.minimum, all_bets_amount)):
            raise InvalidBet(f'Bet amounts should not be less than tabel minimum {self.minmum}')
    

class Passenger57:
    
    def __init__(self, table: Table, wheel: Wheel):
        self.table = table
        self.wheel = wheel
        self.black = wheel.get_outcome('Black')
        self.bet = Bet(200, self.black)
    
    def place_bet(self):
        table.place_bet(self.bet) 
        
           
    def win(self, bet: Bet):
        if bet == self.bet:
            print('You win')
    
    
    def lose(self, bet: Bet):
        if bet.outcome == self.bet.outcome:
            print('You lose')


class Game:
    """manages the sequence of actions that defines the game of Roulette"""
    
    def __init__(self, wheel: Wheel, table: Table):
        self.wheel = wheel
        self.table = table 
        
    def cycle(self, player: Passenger57):
        player.place_bet()
        winning_bets = self.wheel.choose()
        
        bets = iter(self.table)
        for bet in bets:
            if bet.outcome in winning_bets:
                player.win(bet)
            else:
                player.lose(bet)


if __name__ == "__main__":
    wheel = Wheel()
    table = Table()
    bin_builder = BinBuilder()
    bin_builder.build_even_money_bets(wheel, Outcome)
    player57 = Passenger57(table, wheel)
    game = Game(wheel, table)
    game.cycle(player57)