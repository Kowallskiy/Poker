import random
import itertools
from collections import defaultdict

RANK = "AKQJT98765432"
SUIT = "cdhs"
DECK = list(''.join(card) for card in itertools.product(RANK, SUIT))
deck = DECK[:]

def number_of_players():
    while True:
        players = input("How many players are going to play at the table? ")
        if players.isdigit() and int(players) in range(2, 7):
            return int(players)
        else:
            print("Invalid number of players")

def deposit():
    while True:
        deposit = input("How much do you want to deposit? The minimum deposit is $100 and maximum is $10000.  $")
        if deposit.isdigit() and int(deposit) in range(100, 10001):
            return int(deposit)
        else:
            print("Please enter a valid number")

def tables():
    print("There are 3 tables available for playing. The first requires $100 to buy-in, the second - $1000, and the last one - $10000")
    while True:
        table = input('At what table do you want to play? (1) - $100, (2) - $1000, (3) - $10000 ')
        if table.isdigit() and int(table) in range(1, 4):
            return int(table)
        else:
            print("Wrong table")

def cards_dealing(players):
    players_cards = []
    for _ in range(players):
        x = random.sample(deck, 2)
        for i in x:
            deck.remove(i)
        players_cards.append(x)
    print(players_cards)
    return players_cards

# There must be a better way to write this function. Optimize it 
def bet_preflop(table, balance):
    if table == 1:
        while True:
            bet = input("What is your bet? $")
            if bet.isdigit() and 1 <= int(bet) <= balance:
                return int(bet)
            else:
                if bet.isdigit() == False:
                    print("Please, enter a number")
                elif int(bet) < 1:
                    print('You cannot bet less than $1')
                elif int(bet) > balance:
                    print(f"You do not have that much to bet. Your balance is ${balance}")
    elif table == 2:
        while True:
            bet = input("What is your bet? $")
            if bet.isdigit() and 10 <= int(bet) <= balance:
                return int(bet)
            else:
                if bet.isdigit() == False:
                    print("Please, enter a number")
                elif int(bet) < 10:
                    print('You cannot bet less than $10')
                elif int(bet) > balance:
                    print(f"You do not have that much to bet. Your balance is ${balance}")
    elif table == 3:
        while True:
            bet = input("What is your bet? $")
            if bet.isdigit() and 100 <= int(bet) <= balance:
                return int(bet)
            else:
                if bet.isdigit() == False:
                    print("Please, enter a number")
                elif int(bet) < 100:
                    print('You cannot bet less than $100')
                elif int(bet) > balance:
                    print(f"You do not have that much to bet. Your balance is ${balance}")

def flop():
    flop = random.sample(deck, 3)
    for i in flop:
        deck.remove(i)
    print(flop)
    return flop

def tern(tern):
    x = random.choice(deck)
    tern.append(x)
    deck.remove(x)
    print(tern)
    return tern

def river(river):
    x = random.choice(deck)
    river.append(x)
    deck.remove(x)
    print(river)
    return river

def combinations(players_cards, river):
    ranks_count = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}

    cards = players_cards[0] + river
    print(cards)

    # Finish it later
    def check_royal_flash(cards):
        values_r = [i[0] for i in cards]
        values_s = [i[1] for i in cards]
        values_count = defaultdict(lambda: 0)
        pass

    def street_flash(cards):
        if check_flush(cards) and check_street(cards):
            return True
        else:
            return False
        
    def check_four_of_a_kind(cards):
        value = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in value:
            value_counts[v] += 1
        if sorted(value_counts.value) == [1, 4]:
            return True
        else:
            return False
        
    def check_full_house(cards):
        value = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in value:
            value_counts[v] += 1
        if sorted(value_counts.value) == [2, 3]:
            return True
        else:
            return False
        
    def check_flush(cards):
        value = [i[1] for i in cards]
        
        if len(set(value)) == 1:
            return True
        else:
            return False
        
        # I wrote it for 5 cards, but my variable cards consists of 7 cards
        # which means it is not going to work. I need to fix it later
    def check_street(cards):
        value = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in value:
            value_counts[v] += 1
        rank_score = [ranks_count[i] for i in value]
        rank_range = max(rank_score) - min(rank_score)
        if rank_range == 4 and len(set(value_counts.value)) == 1:
            return True
        else:
            return False
        
    def check_three_of_a_kind(cards):
        values = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values) == [1, 3]:
            return True
        else:
            return False
        
    def check_check_two_pairs(cards):
        value = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in value:
            value_counts[v] += 1
        if sorted(value_counts.value) == [2, 2]:
            return True
        else:
            return False
        
    def check_one_pair(cards):
        value = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in value:
            value_counts[v] += 1
        if sorted(value_counts.value) == [1, 2]:
            return True
        else:
            return False

    pass
    
def main():
    balance = deposit()
    table = tables()
    players = number_of_players()
    players_cards = cards_dealing(players)
    bet_preflop(table, balance)
    flopp = flop()
    ter = tern(flopp)
    riv = river(ter)
    combinations(players_cards, riv)

main()