from roulette import Outcome, Wheel, Bin, BinBuilder

def test_outcome():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Red", 1)
    o3 = Outcome("Black", 2)
    
    assert str(o1) == "Red 1:1"
    assert repr(o2) == "Outcome(name='Red', odds=1)"
    assert o1 == o2
    assert o1.odds == 1
    assert o1.name == "Red"
    assert o1 != o3
    assert o2 != o3

def test_wheel_sequence():
    wheel = Wheel()
    wheel.add_outcome(8, {Outcome("test", 1)})
    wheel.randgenerator.seed(1)
    assert Outcome("test", 1) in wheel.choose()
   
def test_bin_builder():
    wheel = Wheel()
    bin_builder = BinBuilder()
    #straightbet test 
    bin_builder.build_straight_bet(wheel, Outcome)
    assert Outcome('0', 35) in wheel.get(0)
    assert Outcome('00', 35) in  wheel.get(37)
    assert Outcome('1', 35) in wheel.get(1)
    assert Outcome('36', 35) in wheel.get(36)
    
    #splitbet test
    wheel = Wheel()
    bin_builder.build_split_bet(wheel, Outcome)
    assert Outcome('1-2', 17) in wheel.get(1)
    assert Outcome('1-4', 17) in wheel.get(1)
    assert Outcome('33-36', 17) in wheel.get(36)
    assert Outcome('35-36', 17) in wheel.get(36)
    
    #streetbet
    wheel = Wheel()
    bin_builder.build_street_bet(wheel, Outcome)
    assert Outcome('1-2-3', 11) in wheel.get(1)
    assert Outcome('34-35-36', 11) in wheel.get(36)
    
    #Cornerbet
    wheel = Wheel()
    bin_builder.build_corner_bets(wheel, Outcome)
    assert Outcome('1-2-4-5', 8) in wheel.get(1)
    assert Outcome('4-5-7-8', 8) in wheel.get(4)
    assert Outcome('5-6-8-9', 8) in wheel.get(5)
    
    #linebet
    wheel = Wheel()
    bin_builder.build_line_bets(wheel, Outcome)
    assert Outcome('1-2-3-4-5-6', 5) in wheel.get(1)
    assert 1 == len(wheel.get(1))
    assert Outcome('1-2-3-4-5-6', 5) in wheel.get(4)
    assert Outcome('4-5-6-7-8-9', 5) in wheel.get(4)
    
    # dozen bet
    wheel = Wheel()
    bin_builder.build_dozen_bets(wheel, Outcome)
    assert Outcome('1-dozen', 2) in wheel.get(1)
    assert Outcome('2-dozen', 2) in wheel.get(17)
    assert Outcome('3-dozen', 2) in wheel.get(36)
    
    #column bet
    wheel = Wheel()
    bin_builder.build_column_bets(wheel, Outcome)
    assert Outcome('1-column', 2) in wheel.get(1)
    assert Outcome('2-column', 2) in wheel.get(17)
    assert Outcome('3-column', 2) in wheel.get(36)
    
    #evenbet
    wheel = Wheel()
    bin_builder.build_even_money_bets(wheel, Outcome)
    assert Outcome('Red', 1) in wheel.get(1)
    assert Outcome('Low', 1) in wheel.get(1)
    assert Outcome('Odd', 1) in wheel.get(1)
    assert Outcome('Black', 1) in wheel.get(17)
    assert Outcome('Low', 1) in wheel.get(17)
    assert Outcome('Odd', 1) in wheel.get(17)
    assert Outcome('Black', 1) in wheel.get(17)
    assert Outcome('Red', 1) in wheel.get(18)
    assert Outcome('Even', 1) in wheel.get(18)
    assert Outcome('Low', 1) in wheel.get(18)
    assert Outcome('Red', 1) in wheel.get(36)
    assert Outcome('Even', 1) in wheel.get(36)
    assert Outcome('High', 1) in wheel.get(36)

    #fivebet
    wheel = Wheel()
    bin_builder.build_five_bet(wheel, Outcome)
    assert Outcome('00-0-1-2-3', 6) in wheel.get(0)
    assert Outcome('00-0-1-2-3', 6) in wheel.get(37)
