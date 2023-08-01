import random
import itertools
from collections import defaultdict

RANK = "AKQJT98765432"
SUIT = "cdhs"
DECK = list(''.join(card) for card in itertools.product(RANK, SUIT))
# deck = DECK[:]
hand_dict = {9:"straight-flush", 8:"four-of-a-kind", 7:"full-house", 6:"flush", 5:"straight", 4:"three-of-a-kind", 3:"two-pairs", 2:"one-pair", 1:"highest-card"}

# I think I will delete this function because it is going to be heads-up
def number_of_players():
    while True:
        players = input("How many players are going to play at the table? ")
        if players.isdigit() and int(players) in range(2, 7):
            return int(players)
        else:
            print("Invalid number of players")

# This function asks a player how much he/she wants to deposit
def deposit():
    while True:
        deposit = input("How much do you want to deposit? The minimum deposit is $200 and maximum is $10000.  $")
        if deposit.isdigit() and int(deposit) in range(200, 10001):
            return int(deposit)
        else:
            print("Please enter a valid number")

# This function receives an information about what table the players wants to join
def tables():
    print("There are 3 tables available for playing. The first requires $100 to buy-in, the second - $1000, and the last one - $10000")
    while True:
        table = input('At what table do you want to play? (1) - $200, (2) - $1000, (3) - $10000 ')
        if table.isdigit() and int(table) in range(1, 4):
            return int(table)
        else:
            print("Wrong table")

# This function randomly deals cards to players. I decided it will be heads-up battle,
# so i will delete this players variable or make it constant
def cards_dealing(players):
    players_cards = []
    deck = DECK[:]
    for _ in range(players):
        x = random.sample(deck, 2)
        for i in x:
            deck.remove(i)
        players_cards.append(x)
    print(players_cards)
    return players_cards, deck

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

# This function receives an information about what the player is going to do preflop:
# call, raise or fold, and returns updated bank, balance, and action
def preflop_round(small_blind, bank, balance, opponents_balance):
    while True:
        first_round = input('You are small blind. Do you want to call, raise or fold? ')
        if first_round.lower() == 'call':
            opponents_balance -= 2 * small_blind
            bank += small_blind
            balance -= small_blind
            return bank, first_round.lower(), balance, opponents_balance
        elif first_round.lower() == 'raise':
            opponents_balance -= 2 * small_blind
            return bank, first_round.lower(), balance, opponents_balance
        elif first_round.lower() == 'fold':
            opponents_balance += bank - 2 * small_blind
            balance -= small_blind
            return bank, first_round.lower(), balance, opponents_balance
        else:
            print("Invalid input")

def round_f(answer, bank, balance, opponents_balance, big_blind):
    if answer == 'call':
        # Write how the opponent will respond to player's call
        if 0 <= random.random() <= 0.85:
            print("The opponent checks.")
            print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
            print(f"The bank is ${bank}")
            return bank, balance, opponents_balance, False
        elif 0.85 < random.random() < 1:
            bank, balance, opponents_balance, folded = rise(bank, opponents_balance, balance, big_blind)
            return bank, balance, opponents_balance, folded
    elif answer == 'raise':
        while True:
            raise_ = input("How much do you want to raise? $")
            if raise_.isdigit() and 2 < int(raise_) <= balance:
                bank += int(raise_)
                balance -= int(raise_)
                print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                print(f"The bank is ${bank}")
                break
            else:
                print("Invalid raise")
        if 0 <= random.random() < 0.5:
            if opponents_balance < int(raise_):
                print(f"The opponent called with his last money ${opponents_balance}")
                bank += opponents_balance
                opponents_balance = 0
                print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                print(f"The bank is ${bank}")
                return bank, balance, opponents_balance, False
            else:
                print(f"The opponent called ${raise_}")
                bank += int(raise_)
                opponents_balance -= int(raise_)
                print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                print(f"The bank is ${bank}")
                return bank, balance, opponents_balance, False
        else:
            print('Opponent folded')
            balance += bank
            return bank, balance, opponents_balance, True
    pass

# This function receives an action from the player on the cmall blind after he/she saw the flop
def round_after_preflop():
    while True:
        first_round = input('You are small bilnd. Do you want to check or bet? ')
        if first_round.lower() == 'check':
            return first_round.lower()
        elif first_round.lower() == 'bet':
            return first_round.lower()
        else:
            print("Invalid input")

def opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind):
    if answer == 'check':
        if 0 <= random.random() <= 0.3:
            print('The opponent checks')
            print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
            print(f"The bank is ${bank}")
            return balance, opponents_balance, bank, False
        else:
            if opponents_balance >= 3 * big_blind:
                print(f"The opponent bets ${3*big_blind}")
                bank += 3*big_blind
                opponents_balance -= 3*big_blind
                print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                print(f"The bank is ${bank}")
            else:
                print(f"The opponent bets the last ${opponents_balance}")
                bank += opponents_balance
                last_bet = opponents_balance
                opponents_balance = 0
                print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                print(f"The bank is ${bank}")
            if opponents_balance == 0:
                response = input(f"The opponent bets last ${last_bet}. Do you want to call or fold? ")
                while True:
                    if response.lower() == 'call':
                        bank += last_bet
                        balance -= last_bet
                        print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                        print(f"The bank is ${bank}")
                        return balance, opponents_balance, bank, False
                    elif response.lower() == 'fold':
                        opponents_balance += bank
                        print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                        print(f"The bank is ${bank}")
                        return balance, opponents_balance, bank, True
                    else:
                        print("Invalid response")
            else:
                # CHeck whether somebody folded
                response = input(f"The opponent bet ${3*big_blind}. Do you want to call, reraise or fold? ")
                bank, balance, opponents_balance, folded = opponent_bets(response, big_blind, bank, balance, opponents_balance)
                print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                print(f"The bank is ${bank}")
                if folded == True:
                    return balance, opponents_balance, bank, True
                else:
                    return balance, opponents_balance, bank, False
    elif answer == 'bet':
        while True:
            response = input("How much do you want to bet? $")
            if response.isdigit() and int(response) >= 2:
                bank += int(response)
                balance -= int(response)
                print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                print(f"The bank is ${bank}")
                break
            else:
                print('Invalid bet!')
        if 0 <= random.random() < 0.25:
            print('Opponent folded')
            balance += bank
            return balance, opponents_balance, bank, True
        elif 0.25 <= random.random() < 0.75:
            print(f"The opponent called ${response}")
            bank += int(response)
            opponents_balance -= int(response)
            print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
            print(f"The bank is ${bank}")
            return balance, opponents_balance, bank, False
        else:
            bank, balance, opponents_balance, folded = rise(bank, opponents_balance, balance, int(response))
            print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
            print(f"The bank is ${bank}")
            return bank, balance, opponents_balance, folded

# The player's response to the opponent's bet
def opponent_bets(answer, big_blind, bank, balance, opponents_balance):
    while True:
        if answer.lower() == 'call':
            balance -= 3 * big_blind
            bank += 3 * big_blind
            print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
            print(f"The bank is ${bank}")
            return bank, balance, opponents_balance, False
        elif answer.lower() == 'reraise':
            while True:
                reraise = input("How much do you want to reraise? ")
                if reraise.isdigit() and 3*big_blind < int(reraise) <= balance:
                    print(f"Your reraise is ${reraise}")
                    balance -= int(reraise)
                    bank += int(reraise)
                    if 0 < random.random() <= 0.5 and opponents_balance >= int(reraise):
                        print(f"The opponent called ${reraise}")
                        bank += int(reraise)
                        opponents_balance -= int(reraise)
                        print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
                        print(f"The bank is ${bank}")
                        return bank, balance, opponents_balance, False
                    else:
                        print("The opponent folded")
                        balance += bank
                        return bank, balance, opponents_balance, True
                else:
                    print("Invalid reraise")
        elif answer.lower() == 'fold':
            opponents_balance += bank
            return bank, balance, opponents_balance, True
        else:
            print("Invalid action")

# I must come up with how I will play against simple AI. How can i realize it?
# It might be a good idea to use class for the opponent
def heads_up_1st_table(depos, players, balance):
    small_blind = 1
    big_blind = 2
    opponents_balance = 200
    while True:
        bank = 3
        players_cards, deck = cards_dealing(players)
        bank, answer, balance, opponents_balance = preflop_round(small_blind, bank, balance, opponents_balance)
        if answer == 'fold':
            continue
        bank, balance, opponents_balance, folded = round_f(answer, bank, balance, opponents_balance, big_blind)
        if folded == True:
            continue
        # I will have to optimize it. Probably create another function
        # Yeah, it has been decided. It is going to be a function
        if balance == 0 or opponents_balance == 0:
            print(f"Your balance is ${balance}. The opponent's balance is ${opponents_balance}")
            print(f"The bank is ${bank}")
            flopp, deck = flop(deck)
            riv, deck = tern(flopp, deck)
            dec = river(riv, deck)
            players_best_combination, players_score = play(players_cards[0], dec)
            opponents_best_combination, opponents_score = play(players_cards[1], dec)

            print(f"You have {players_best_combination}, the opponent has {opponents_best_combination}")
            print(f"The deck is {dec}")
            if players_score > opponents_score:
                print(f"You won ${bank}")
                balance += bank
            elif opponents_score > players_score:
                print(f"The opponent won ${bank}")
                opponents_balance += bank
            else:
                print(f"It is a tie.")
                balance += bank / 2
                opponents_balance += bank / 2
                
            if opponents_balance == 0:
                bool = zero_balance_opponent(opponents_balance)
                if bool == True:
                    continue
                else:
                    return
            elif balance == 0:
                bool = zero_balance_player(depos)
                if bool == True:
                    balance = 200
                    depos -= balance
                else:
                    return
            else:
                continue
        flopp, deck = flop(deck)
        answer = round_after_preflop()
        balance, opponents_balance, bank, folded = opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind)
        if folded == True:
            continue
        riv, deck = tern(flopp, deck)
        answer = round_after_preflop()
        balance, opponents_balance, bank, folded = opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind)
        if folded == True:
            continue
        dec = river(riv, deck)
        answer = round_after_preflop()
        balance, opponents_balance, bank, folded = opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind)
        if folded == True:
            continue
        players_best_combination, players_score = play(players_cards[0], dec)
        opponents_best_combination, opponents_score = play(players_cards[1], dec)

        print(f"You have {players_best_combination}, the opponent has {opponents_best_combination}")
        print(f"The deck is {dec}")
        if players_score > opponents_score:
            print(f"You won ${bank}")
            balance += bank
        elif opponents_score > players_score:
            print(f"The opponent won ${bank}")
            opponents_balance += bank
        else:
            print(f"It is a tie.")
            balance += bank / 2
            opponents_balance += bank / 2

        if opponents_balance == 0:
            bool = zero_balance_opponent(opponents_balance)
            if bool == True:
                continue
            else:
                return
        elif balance == 0:
            bool = zero_balance_player(depos)
            if bool == True:
                balance = 200
                depos -= balance
            else:
                return
            
def zero_balance_opponent(opponents_balance):
    while True:
        another_op = input('The opponent lost all his money. Do you want to play against another one (yes/no)? ')
        if another_op.lower() == 'yes':
            opponents_balance == 200
            return True
        elif another_op.lower() == 'no':
            return False
        else:
            print('Invalid response')

def zero_balance_player(depos):
    while True:
        play_again = input("You lost your money. Do you want to play again (yes/no)? ")
        if play_again == 'no':
            return False
        elif play_again == 'yes':
            if depos >= 200:
                return True
            else:
                print(f'Unfortunately you do not have enough money to buy in. You have only ${depos}.')
                print('You need $200 to play.')
                return False
        else:
            print('Invalid response')

# The opponent raises his bet!
# I think I must make sure that the opponent will not bet more than he has
def rise(bank, opponents_balance, balance, big_blind):
    print(f"The opponent raises ${3 * big_blind}")
    opponents_balance -= 3 * big_blind
    bank += 3 * big_blind
    while True:
        answer = input(f"Do you want to call ${3 * big_blind}, reraise or fold? ")
        if answer.lower() == 'call':
            balance -= 3 * big_blind
            bank += 3 * big_blind
            return bank, balance, opponents_balance, False
        elif answer.lower() == 'reraise':
            while True:
                reraise = input("How much do you want to reraise? $")
                if reraise.isdigit() and 3*big_blind < int(reraise) <= balance:
                    print(f"Your reraise is ${reraise}")
                    balance -= int(reraise)
                    bank += int(reraise)
                    if 0 < random.random() <= 0.5 and opponents_balance >= int(reraise):
                        print(f"The opponent called ${reraise}")
                        bank += int(reraise)
                        opponents_balance -= int(reraise)
                        return bank, balance, opponents_balance, False
                    else:
                        print("The opponent folded")
                        balance += bank
                        return bank, balance, opponents_balance, True
                else:
                    print("Invalid reraise")
        elif answer.lower() == 'fold':
            opponents_balance += bank
            return bank, balance, opponents_balance, True
        else:
            print("Invalid action")

# This function deals flop cards
def flop(deck):
    flop = random.sample(deck, 3)
    for i in flop:
        deck.remove(i)
    print(flop)
    return flop, deck

# This function deals tern card
def tern(tern, deck):
    x = random.choice(deck)
    tern.append(x)
    deck.remove(x)
    print(tern)
    return tern, deck

# This function deals river card
def river(river, deck):
    x = random.choice(deck)
    river.append(x)
    deck.remove(x)
    print(river)
    return river

# This function checks all possible combinations. It is not finished 
def combination(cards):
    ranks_count = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    
    # Finish it later
    def check_royal_flash(cards):
        values_r = [i[0] for i in cards]
        values_s = [i[1] for i in cards]
        values_count = defaultdict(lambda: 0)
        pass

    def check_street_flush(cards):
        if check_flush(cards) and check_street(cards):
            return True
        else:
            return False
        
    def check_four_of_a_kind(cards):
        values = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 4]:
            return True
        else:
            return False
        
    def check_full_house(cards):
        values = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [2, 3]:
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
        values = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        rank_score = [ranks_count[i] for i in values]
        rank_range = max(rank_score) - min(rank_score)
        if rank_range == 4 and len(set(value_counts.values())) == 1:
            return True
        else:
            if set(values) == set(['A', '2', '3', '4', '5']):
                return True
            return False
        
    def check_three_of_a_kind(cards):
        values = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 1, 3]:
            return True
        else:
            return False
        
    def check_two_pairs(cards):
        values = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 2, 2]:
            return True
        else:
            print(sorted(value_counts.values()))
            return False
        
    def check_one_pair(cards):
        values = [i[0] for i in cards]
        value_counts = defaultdict(lambda: 0)
        for v in values:
            value_counts[v] += 1
        if sorted(value_counts.values()) == [1, 1, 1, 2]:

            return True
        else:
            return False
    
    if check_street_flush(cards) == True:
        return 9
    elif check_four_of_a_kind(cards) == True:
        return 8
    elif check_full_house(cards) == True:
        return 7
    elif check_flush(cards) == True:
        return 6
    elif check_street(cards) == True:
        return 5
    elif check_three_of_a_kind(cards) == True:
        return 4
    elif check_two_pairs(cards) == True:
        return 3
    elif check_one_pair(cards) == True:
        return 2
    else:
        return 1

def play(hand, dec):
    # The riv variable is a deck containing 7 cards, 2 from the player and 5 from 3 rounds of playing
    riv = hand + dec
    best_hand = 0
    possible_combos = itertools.combinations(riv, 5)
    possible_combos = list(possible_combos)
    
    for c in possible_combos:
        current_hand = list(c)
        print(current_hand)
        hand_value = combination(current_hand)
        if hand_value > best_hand:
            best_hand = hand_value
    return hand_dict[best_hand], best_hand

# There will be significant changes in the main function, but I will fix it later
def main():
    depos = deposit()
    table = tables()
    players = number_of_players()
    
    if players == 2:
        if table == 1:
            balance = 200
            depos -= balance
            heads_up_1st_table(depos, players, balance)
        elif table == 2:
            heads_up_2nd_table()
        elif table == 3:
            heads_up_3d_table()

main()