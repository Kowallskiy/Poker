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
    if s in pairs:
        print('Yes')
    else:
        print("no")
pairs()