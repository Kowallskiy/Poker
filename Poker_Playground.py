import random
import itertools
from collections import defaultdict

PLAYERS = 2
RANK = "AKQJT98765432"
SUIT = "cdhs"
DECK = list(''.join(card) for card in itertools.product(RANK, SUIT))
ranks_count = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
hand_dict = {9:"straight-flush", 8:"four-of-a-kind", 7:"full-house", 6:"flush", 5:"straight", 4:"three-of-a-kind", 3:"two-pairs", 2:"one-pair", 1:"highest-card"}

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

# This function receives an information about what the player is going to do preflop:
# call, raise or fold, and returns updated bank, balance, and action
def preflop_round(small_blind, bank, balance, opponents_balance, position):
    if position % 2 == 1:
        while True:
            first_round = input('You are small blind. Do you want to call, raise or fold? ')
            if first_round.lower() == 'call':
                opponents_balance -= 2 * small_blind
                bank += small_blind
                balance -= 2 * small_blind
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
    else:
        if 0 <= random.random() <= 0.2:
            print("Opponent folded.")
            balance += bank
            return bank, response, balance, opponents_balance
        elif 0.2 < random.random() <= 0.8:
            print(f"Opponent called ${small_blind}")
            opponents_balance -= small_blind
            bank += small_blind
            while True:
                response = input("Do you want to check or raise? ")
                if response != 'check' or response != 'raise':
                    print('Invalid response')
                else: break
            return bank, response, balance, opponents_balance
        else:
            print(f"Opponent raised ${6*small_blind}")
            opponents_balance -= 5 * small_blind
            bank += 5 * small_blind
            while True:
                response = input(f"Do you want to call ${4*small_blind}, reraise or fold? ")
                if response == 'call' or response == 'reraise' or response == 'fold':
                    break
                else: print("Invalid response")
            return bank, response, balance, opponents_balance

def on_button(bank, response, balance, opponents_balance, small_blind):
    if response == 'check':
        return bank, balance, opponents_balance, False
    elif response == 'call':
        if balance >= 4*small_blind:
            print(f"You called ${4*small_blind}")
            balance -= 4*small_blind
            bank += 4*small_blind
            return bank, balance, opponents_balance, False
        else:
            print(f"You called with your last ${balance}")
            bank += 2 * balance - 4*small_blind
            opponents_balance += 4*small_blind - balance
            balance = 0
            return bank, balance, opponents_balance, False
    elif response == 'raise':
        while True:
            response = input("How much do you want to raise? $")
            if int(response) <= balance:
                print(f"You raised ${response}")
                if opponents_balance >= int(response):
                    if 0 <= random.random() <= 0.6:
                        print(f"Opponent called ${response}")
                        opponents_balance -= int(response)
                        balance -= int(response)
                        bank += int(response) * 2
                        return bank, balance, opponents_balance, False
                    else:
                        print("Opponent folded")
                        balance += bank
                        return bank, balance, opponents_balance, True
                else:
                    print(f"Opponent called with his last ${opponents_balance}")
                    bank += 2 * opponents_balance
                    balance -= opponents_balance
                    opponents_balance = 0
                    return bank, balance, opponents_balance, False
            elif int(response) > balance:
                print(f"You do not have that much to raise. Your balance: ${balance}")
            else: print("Invalid response")
    elif response == 'reraise':
        while True:
            reraise = input("How much do you want to reraise? ")
            if 6*small_blind < int(reraise) <= balance:
                print(f"You reraised ${reraise}")
                balance -= int(reraise)
                bank += int(reraise)
                if opponents_balance >= int(reraise) - 5*small_blind:
                    if 0 <= random.random() <= 0.5:
                        print{f"Opponent called ${int(reraise)-5*small_blind}"}
                        bank += int(reraise) - 5*small_blind
                        opponents_balance -= int(reraise) + 5 * small_blind
                        return bank, balance, opponents_balance, False
                    else:
                        print("Opponent folded")
                        balance += bank
                        return bank, balance, opponents_balance, True
                else:
                    if 0 <= random.random() <= 0.5:
                        print{f"Opponent called with his last ${opponents_balance}"}
                        bank += opponents_balance + 5*small_blind
                        balance += int(reraise) - opponents_balance
                        opponents_balance = 0
                        return bank, balance, opponents_balance, False
                    else:
                        print("Opponent folded")
                        balance += bank
                        return bank, balance, opponents_balance, True
            elif int(response) > balance:
                print(f"You do not have that much to reraise. Your balance: ${balance}")
            else: print("Invalid response")
    elif response == 'fold':
        print('You folded')
        opponents_balance += bank
        return bank, balance, opponents_balance, True




def round_f(answer, bank, balance, opponents_balance, big_blind):
    while True:
        if answer == 'call':
            # Write how the opponent will respond to player's call
            if 0 <= random.random() <= 0.85:
                print("The opponent checks.")
                print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                print(f"The bank: ${bank}")
                return bank, balance, opponents_balance, False
            # I have to fix it, because it is raise, but I used rise function for reraise
            elif 0.85 < random.random() < 1:
                bank, balance, opponents_balance, folded = rise(bank, opponents_balance, balance, big_blind)
                return bank, balance, opponents_balance, folded
        elif answer == 'raise':
            while True:
                raise_ = input("How much do you want to raise? $")
                if raise_.isdigit() and 2 < int(raise_) <= balance:
                    bank += int(raise_) - 1
                    balance -= int(raise_) + 1
                    print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                    print(f"The bank: ${bank}")
                    break
                elif int(raise_) > balance:
                    print(f"You do not have that much money. Your balance: {balance}")
                else: print("Invalid raise")
            if 0 <= random.random() < 0.5:
                if opponents_balance < int(raise_) - 2:
                    print(f"The opponent called with his last money ${opponents_balance}")
                    bank += 2 * opponents_balance - int(raise_) - 2
                    balance += int(raise_) - opponents_balance - 2
                    opponents_balance = 0
                    print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                    print(f"The bank: ${bank}")
                    return bank, balance, opponents_balance, False
                else:
                    print(f"The opponent called ${raise_}")
                    bank += int(raise_) - 2
                    opponents_balance -= int(raise_) + 2
                    print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                    print(f"The bank: ${bank}")
                    return bank, balance, opponents_balance, False
            else:
                print('Opponent folded')
                balance += bank
                return bank, balance, opponents_balance, True
        else:
            print('Invalid action')

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

def opponent_on_button_after_preflop():
    if 0 <= random.random() <= 0.3:
        print('Opponent checks')
        while True:
            response = input('Do you want to check or bet? ')
            if response.lower() == 'check':
                return response.lower()
            elif response.lower() == 'bet':
                return response.lower()
            else:
                print("Invalid input")
    else:
        print(f"Opponent bets ${str(int(0.7 * bank))}")
        while True:
            response = input(f"Do you want to call ${str(int(0.7 * bank))}, reraise or fold? ")
            if response.lower() == 'call' or response.lower() == 'reraise' or response.lower() == 'fold':
                return response.lower()
            else: print("Invalid response")

def opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind):
    if answer == 'check':
        if 0 <= random.random() <= 0.3:
            print('The opponent checks')
            print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
            print(f"The bank: ${bank}")
            return balance, opponents_balance, bank, False
        else:
            if opponents_balance >= bank and balance >= bank:
                bank_bet = bank
                print(f"The opponent bets ${bank_bet}")
                bank += bank_bet
                opponents_balance -= bank_bet
            elif opponents_balance >= balance and balance < bank:
                print(f"Opponent bets ${balance}")
                bank += balance
                opponents_balance -= balance
                while True:
                    response = input(f"Do you want to call with your last ${balance} or fold? ")
                    if response == 'call':
                        bank += balance
                        balance = 0
                        return balance, opponents_balance, bank, False
                    elif response == 'fold':
                        opponents_balance += bank
                        return balance, opponents_balance, bank, True
                    else: print("Invalid response.")
            else:
                print(f"The opponent bets his last ${opponents_balance}")
                bank += opponents_balance
                last_bet = opponents_balance
                opponents_balance = 0
                print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                print(f"The bank: ${bank}")
            if opponents_balance == 0:
                if balance <= last_bet:
                    while True:
                        response = input(f"You have only ${balance}. Do you want to call of fold? ")
                        if response == 'call':
                            bank += 2 * balance - last_bet
                            opponents_balance += last_bet - balance
                            balance = 0
                            return balance, opponents_balance, bank, False
                        elif response == 'fold':
                            opponents_balance += bank
                            return balance, opponents_balance, bank, False
                        else:
                            print("Invalid response")
                else:
                    while True:
                        response = input(f"Do you want to call ${last_bet} or fold? ")
                        if response.lower() == 'call':
                            bank += last_bet
                            balance -= last_bet
                            print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                            print(f"The bank: ${bank}")
                            return balance, opponents_balance, bank, False
                        elif response.lower() == 'fold':
                            opponents_balance += bank
                            print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                            print(f"The bank: ${bank}")
                            return balance, opponents_balance, bank, True
                        else:
                            print("Invalid response")
            else:
                while True:
                    response = input(f"The opponent bet ${bank_bet}. Do you want to call, reraise or fold? ")
                    if response == 'call' or response == 'reraise' or response == 'fold':
                        break
                    else: print("Invalid response.")
                bank, balance, opponents_balance, folded = opponent_bets(response, bank_bet, bank, balance, opponents_balance)
                if folded == True:
                    return balance, opponents_balance, bank, True
                else:
                    return balance, opponents_balance, bank, False
    elif answer == 'bet':
        while True:
            response = input("How much do you want to bet? $")
            if response.isdigit() and 2 <= int(response) <= balance and int(response) <= opponents_balance:
                bank += int(response)
                balance -= int(response)
                print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                print(f"The bank: ${bank}")
                break
            elif balance < int(response):
                print(f"You do not have that much to bet. Balance: ${balance}")
            else:
                print('Invalid bet!')
        if 0 <= random.random() < 0.25:
            print('Opponent folded')
            balance += bank
            return balance, opponents_balance, bank, True
        elif 0.25 <= random.random() < 0.75:
            if opponents_balance < int(response):
                print(f"The opponent called with his last ${opponents_balance}")
                bank += 2 * opponents_balance - int(response)
                balance += int(response) - opponents_balance
                opponents_balance = 0
                return balance, opponents_balance, bank, False
            else:
                print(f"The opponent called ${response}")
                bank += int(response)
                opponents_balance -= int(response)
                print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                print(f"The bank: ${bank}")
                return balance, opponents_balance, bank, False
        else:
            bank, balance, opponents_balance, folded = rise(bank, opponents_balance, balance, int(response))
            return bank, balance, opponents_balance, folded

# The player's response to the opponent's bet
def opponent_bets(answer, bet, bank, balance, opponents_balance):
    if answer.lower() == 'call':
        if balance < bet:
            print(f"You called with your last ${balance}")
            bank += 2 * balance - bet
            opponents_balance += bet - balance
            balance = 0
            return bank, balance, opponents_balance, False
        else:
            balance -= bet
            bank += bet
            print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
            print(f"The bank: ${bank}")
            return bank, balance, opponents_balance, False
    elif answer.lower() == 'reraise':
        while True:
            reraise = input("How much do you want to reraise? $")
            if reraise.isdigit() and balance <= bet:
                print(f"You cannot reraise. You call with your last ${balance}")
                bank += 2 * balance - bet
                opponents_balance += bet - balance
                balance = 0
                return bank, balance, opponents_balance, False
            elif reraise.isdigit() and bet < int(reraise) <= balance:
                print(f"Your reraise is ${reraise}")
                balance -= int(reraise)
                bank += int(reraise)
                if 0 < random.random() <= 0.5 and opponents_balance >= int(reraise):
                    print(f"The opponent called ${reraise}")
                    bank += 2 * int(reraise) - bet
                    opponents_balance -= int(reraise) + bet
                    print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
                    print(f"The bank: ${bank}")
                    return bank, balance, opponents_balance, False
                else:
                    print("The opponent folded")
                    balance += bank
                    return bank, balance, opponents_balance, True
            else:
                print("Invalid reraise")
                continue
    elif answer.lower() == 'fold':
        opponents_balance += bank
        return bank, balance, opponents_balance, True

# I must come up with how I will play against simple AI. How can i realize it?
# It might be a good idea to use class for the opponent
def heads_up_1st_table(depos, players, balance):
    small_blind = 1
    big_blind = 2
    opponents_balance = 200
    position = 1
    while True:
        if opponents_balance == 0:
            opponents_balance = 200
        bank = 3
        players_cards, deck = cards_dealing(players)
        print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
        bank, answer, balance, opponents_balance = preflop_round(small_blind, bank, balance, opponents_balance)
        if answer == 'fold':
            position += 1
            continue
        if position % 2 == 1:
            bank, balance, opponents_balance, folded = round_f(answer, bank, balance, opponents_balance, big_blind)
        else:
            bank, balance, opponents_balance, folded = on_button(bank, answer, balance, opponents_balance, small_blind):
        if folded == True:
            position += 1
            continue
        # I will have to optimize it. Probably create another function
        # Yeah, it has been decided. It is going to be a function
        if balance == 0 or opponents_balance == 0:
            print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
            print(f"The bank: ${bank}")
            flopp, deck = flop(deck)
            riv, deck = tern(flopp, deck)
            dec = river(riv, deck)
            bank, balance, opponents_balance = check_winning(players_cards, dec, balance, bank, opponents_balance)
            position += 1

            if opponents_balance == 0:
                bool = zero_balance_opponent(opponents_balance)
                if bool == True: 
                    opponents_balance == 200
                    continue
                else: return
            elif balance == 0:
                bool = zero_balance_player(depos)
                if bool == True:
                    balance = 200
                    depos -= balance
                    continue
                else: return
        flopp, deck = flop(deck)
        if position % 2 == 1:
            answer = round_after_preflop()
            balance, opponents_balance, bank, folded = opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind)
        else:
            answer = opponent_on_button_after_preflop():
            if answer == 'check' or answer == 'bet':
                
        if folded == True:
            position += 1
            continue
        if balance == 0 or opponents_balance == 0:
            print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
            print(f"The bank: ${bank}")
            riv, deck = tern(flopp, deck)
            dec = river(riv, deck)
            bank, balance, opponents_balance = check_winning(players_cards, dec, balance, bank, opponents_balance)
            position += 1

            if opponents_balance == 0:
                bool = zero_balance_opponent(opponents_balance)
                if bool == True: continue
                else: return
            elif balance == 0:
                bool = zero_balance_player(depos)
                if bool == True:
                    balance = 200
                    depos -= balance
                    continue
                else: return
        riv, deck = tern(flopp, deck)
        answer = round_after_preflop()
        balance, opponents_balance, bank, folded = opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind)
        if folded == True:
            position += 1
            continue
        if balance == 0 or opponents_balance == 0:
            print(f"Your balance: ${balance}. The opponent's balance: ${opponents_balance}")
            print(f"The bank: ${bank}")
            dec = river(riv, deck)
            bank, balance, opponents_balance = check_winning(players_cards, dec, balance, bank, opponents_balance)
            position += 1

            if opponents_balance == 0:
                bool = zero_balance_opponent(opponents_balance)
                if bool == True: 
                    opponents_balance == 200
                    continue
                else: return
            elif balance == 0:
                bool = zero_balance_player(depos)
                if bool == True:
                    balance = 200
                    depos -= balance
                    continue
                else: return
        dec = river(riv, deck)
        answer = round_after_preflop()
        balance, opponents_balance, bank, folded = opponent_after_preflop(answer, balance, opponents_balance, bank, big_blind)
        if folded == True:
            position += 1
            continue
        
        position += 1
        bank, balance, opponents_balance = check_winning(players_cards, dec, balance, bank, opponents_balance)
        
        if opponents_balance == 0:
            bool = zero_balance_opponent(opponents_balance)
            if bool == True: 
                opponents_balance == 200
                continue
            else: return
        elif balance == 0:
            bool = zero_balance_player(depos)
            if bool == True:
                balance = 200
                depos -= balance
                continue
            else: return

def check_winning(players_cards, dec, balance, bank, opponents_balance):
    players_best_combination, players_score = play(players_cards[0], dec)
    opponents_best_combination, opponents_score = play(players_cards[1], dec)

    print(f"You have {players_best_combination}, the opponent has {opponents_best_combination}")
    print(f"The deck is {dec}")
    if players_best_combination == opponents_best_combination:
        if max([ranks_count[key[0]] for key in players_cards[0]]) > max([ranks_count[key[0]] for key in players_cards[1]]):
            print(f"You won ${bank}")
            balance += bank
            return bank, balance, opponents_balance
        elif max([ranks_count[key[0]] for key in players_cards[0]]) < max([ranks_count[key[0]] for key in players_cards[1]]):
            print(f"The opponent won ${bank}")
            opponents_balance += bank
            return bank, balance, opponents_balance
        else:
            print("It is a tie.")
            balance += int(bank / 2)
            opponents_balance += int(bank / 2)
            return bank, balance, opponents_balance
    if players_score > opponents_score:
        print(f"You won ${bank}")
        balance += bank
        return bank, balance, opponents_balance
    elif opponents_score > players_score:
        print(f"The opponent won ${bank}")
        opponents_balance += bank
        return bank, balance, opponents_balance
    else:
        print(f"It is a tie.")
        balance += int(bank / 2)
        opponents_balance += int(bank / 2)
        return bank, balance, opponents_balance
       
def zero_balance_opponent(opponents_balance):
    while True:
        another_op = input('The opponent lost all his money. Do you want to play against another one (yes/no)? ')
        if another_op.lower() == 'yes':
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
def rise(bank, opponents_balance, balance, bet):
    if opponents_balance <= 3*bet:
        print(f"Opponent raises his last ${opponents_balance}")
        bank += opponents_balance
        if balance >= opponents_balance:
            while True:
                response = input(f"Do you want to call ${opponents_balance} or fold? ")
                if response == 'call':
                    bank += opponents_balance
                    balance -= opponents_balance
                    opponents_balance = 0
                    return bank, balance, opponents_balance, False
                elif response == 'fold':
                    opponents_balance = bank
                    return bank, balance, opponents_balance, True
                else:
                    print("Invalid response.")
        else:
            while True:
                response = input(f"You have last ${balance}. Do you want to call or fold? ")
                if response == 'call':
                    bank += 2*balance - opponents_balance
                    opponents_balance += opponents_balance - balance
                    balance = 0
                    return bank, balance, opponents_balance, False
                elif response == 'fold':
                    opponents_balance += bank
                    return bank, balance, opponents_balance, True
                else:
                    print("Invalid response.")
                    continue
    print(f"The opponent raises ${3 * bet}")
    opponents_balance -= 3 * bet
    bank += 3 * bet
    if balance <= 2*bet:
        while True:
            an = input(f"You have last ${balance}.Do you want to call or fold? ")
            if an == 'call':
                bank += 2 * balance - 3 * bet
                opponents_balance += 3*bet - balance
                balance = 0
                return bank, balance, opponents_balance, False
            elif an == 'fold':
                opponents_balance += bank
                return bank, balance, opponents_balance, True
            else:
                print("Invalid input.")
                continue
    else:
        answer = input(f"Do you want to call ${2 * bet}, reraise or fold? ")
        if answer.lower() == 'call':
            # I do not subtract 3*bet because the player already bet 1*bet, so he needs to call only 2*bet
            balance -= 2 * bet
            bank += 2 * bet
            return bank, balance, opponents_balance, False
        elif answer.lower() == 'reraise':
            while True:
                reraise = input("How much do you want to reraise? $")
                if reraise.isdigit() and 3*bet < int(reraise) <= balance:
                    print(f"Your reraise is ${reraise}")
                    balance -= int(reraise) + bet
                    bank += int(reraise) - bet
                    if 0 <= random.random() <= 0.5 and opponents_balance >= int(reraise) - 3*bet:
                        print(f"The opponent called ${reraise}")
                        bank += int(reraise) - 3*bet
                        opponents_balance -= int(reraise) + 3*bet
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
    if table == 1:
        balance = 200
        depos -= balance
        heads_up_1st_table(depos, PLAYERS, balance)
    elif table == 2:
        heads_up_2nd_table()
    elif table == 3:
        heads_up_3d_table()

main()