import random
import itertools

RANK = "AKQJT98765432"
SUIT = "cdhs"

DECK = list(''.join(card) for card in itertools.product(RANK, SUIT))
deck = DECK[:]

x = random.sample(deck, 5)
print(x)
for i in x:
    deck.remove(i)
print(deck)

