import random
import itertools

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

def cards_dealing(players):
    players_cards = []
    for _ in range(players):
        x = random.sample(deck, 2)
        for i in x:
            deck.remove(i)
        players_cards.append(x)
    print(players_cards)

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

def combinations():
    for i in DECK:
    pair = 
    
    
def main():
    players = number_of_players()
    cards_dealing(players)
    flopp = flop()
    ter = tern(flopp)
    river(ter)

main()