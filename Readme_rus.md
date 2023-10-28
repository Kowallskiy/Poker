# Техасский холдем хэдс-ап против ИИ

Язык: [English](README.md), Русский
___
![](Pictures/main_theme.jpg)
___
__Техасский холдем__ является самым популярным видом покера. Раньше я играл за столами с _9_ и _6_ игроками. Однако, спустя некоторое время я решил начать играть в хэдс-ап (игра один на один). Основная разница в динамике игры- это агрессия. В отличие от столов с _9_ и _6_ игроками ты должен играть около __80%__ рук, в зависимости от баланса. Чем ниже баланс, тем агрессивнее должен быть стиль игры из-за ограниченного количества способов защиты своей руки.

Ниже представлен упрощенный чарт рук, разыгрываемых игроком префлоп в хэдс-ап:

![preflop_chart](Pictures/heads_up_preflop_chart.png)

Пассивный розыгрыш этих рук неэффективен. Это означает, что игроку следует периодически поднимать ставку вместо пассивного уравнивания. Учитывая динамику игры, игрок должен поднимать ставку даже если на флопе данную руку будет разыгрывать некомфортно. Ниже представлен чарт рук, с которыми игроку следует поднимать ставку префлоп:

![Alt text](Pictures/preflop_raise.png)

Это означает, что игроку следует поднимать ставку примерно в __25%__ случаев префлоп.

На флопе динамика игры остается агрессивной. Игроку следует делть ставку вместо того, чтобы пропускать ход. Однако его ответный ход на рейзы должен оставаться гибким. Ниже представлен чарт рук, разыгрываемых при ререйзе противника:

![Alt text](Pictures/3bet_chart.png)

Следование данной стратегии является сложной задачей. Гораздо проще играть прямолинейно, но это невыгодно. 
___
# Код 

ИИ в данном проекте не является сложным и может быть значительно улучшен, но это не означает, что против него скучно играть. Добавление условий и понимания ценности карт улучшило бы ИИ. Однако я решил не тратить слишком много времени на написание кода, который я уже знаю как писать, сосредоточившись на правильной работе игры.

Ниже представлен пример того, как ИИ ведёт себя при ререйзе от игрока:

```Python
if opponents_balance >= int(reraise) - 6*small_blind:
    if 0 <= random.random() <= 0.5:
        print(f"Opponent called ${int(reraise)-6*small_blind}")
        bank = bank + int(reraise) - 6*small_blind
        opponents_balance = opponents_balance - int(reraise) + 6 * small_blind
        print(f"Your balance: ${balance}, opponent's balance: ${opponents_balance}")
        print(f"Bank: ${bank}")
```

Можно с легкостью понять стратегию ИИ ознакомившись с данным [кодом](Poker_Playground.py).

Я думаю, что самым сложным было написание функций комбинаций, которые проверяют руку и придают её определенную ценность. Данный код демонстрирует то, как я с этим справился:

```Python
ranks_count = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, 'T': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    
    def check_royal_flash(cards):
        values_r = [i[0] for i in cards]
        if check_flush(cards) and check_street(cards) and sorted(values_r) == ['A', 'J', 'K', 'Q', 'T']:
            return True
        else:
            return False

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

    if check_royal_flash(cards) == True:
        return 10
    elif check_street_flush(cards) == True:
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
```

Ещё одна интересная функция - __play__. Она принимает две переменные: __dec__ - представляет 5 карт со стола со всех раундов игры, и __hand__ - представляет карты с руки игрока или оппонента. Функция генерирует все возможные комбинации из 5-ти карт и возвращает комбинацию с наибольшей ценностью. Ниже представлена данная функция:

```Python
def play(hand, dec):
    # Переменная riv состоит из 7-ми карт: 2 карты игрока/оппонента и 5 карт со стола
    riv = hand + dec
    best_hand = 0
    possible_combos = itertools.combinations(riv, 5)
    possible_combos = list(possible_combos)
    
    for c in possible_combos:
        current_hand = list(c)
        hand_value = combination(current_hand)
        if hand_value > best_hand:
            best_hand = hand_value
    return hand_dict[best_hand], best_hand
```

![gif](https://i.gifer.com/7aKz.gif)