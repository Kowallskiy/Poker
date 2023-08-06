import itertools
from itertools import combinations

RANK = "AKQJT98765432"
SUIT = "cdhs"
DECK = tuple(''.join(card) for card in itertools.product(RANK, SUIT))

def pairs():
    aces = []
    kings = []
    queens = []
    jacks = []
    ten = []
    nine = []
    eight = []
    seven = []
    six = []
    five = []
    four = []
    three = []
    two = []
    parirs = []
    for i in DECK:
        if i.startswith('A'):
            aces.append(i)
        elif i.startswith('K'):
            kings.append(i)
        elif i.startswith('Q'):
            queens.append(i)
        elif i.startswith('J'):
            jacks.append(i)
        elif i.startswith('T'):
            ten.append(i)
        elif i.startswith('9'):
            nine.append(i)
        elif i.startswith('8'):
            eight.append(i)
        elif i.startswith('7'):
            seven.append(i)
        elif i.startswith('6'):
            six.append(i)
        elif i.startswith('5'):
            five.append(i)
        elif i.startswith('4'):
            four.append(i)
        elif i.startswith('3'):
            three.append(i)
        else:
            two.append(i)
    pairs = list(combinations(queens, 2))
    print(pairs)
    s = ['Qd', 'Qh']
    print(set(s).issubset(pairs))
pairs()

# I think I will delete this function because it is going to be heads-up
def number_of_players():
    while True:
        players = input("How many players are going to play at the table? ")
        if players.isdigit() and int(players) in range(2, 7):
            return int(players)
        else:
            print("Invalid number of players")

# There must be a better way to write this function. Optimize it 
# I do not think I will need this function anymore. But I will not delete it yet
def bet_preflop(table, balance):
    if table == 1:
        while True:
            bet = input("What is your bet? $")
            if bet.isdigit() and 2 <= int(bet) <= balance:
                print(f"Your bet is ${int(bet)}")
                return int(bet)
            else:
                if bet.isdigit() == False:
                    print("Please, enter a number")
                elif int(bet) < 2:
                    print('You cannot bet less than $2')
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

s = ['J', 'K', 'A', 'T', 'Q']
print(sorted(s))