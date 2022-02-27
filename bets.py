import math

ODDS_PAYOUT = {4: 2.0, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2.0}
PLACE_PAYOUT = {4: 9.0/5, 5: 7.0/5, 6: 7.0/6, 8: 7.0/6, 9: 7.0/5, 10: 9.0/5}
HARDWAY_PAYOUT = {4: 7, 6: 9, 8: 9, 10: 7}


def any_craps(player, roll, point, bet, total):
    if total in [2, 3, 12]:
        player.bankroll += bet
        player.bankroll += 7 * bet
    player.clear_bet("anycraps")


# Hardways are always off on come out rolls currently
def hardway_gen(x):
    target_dietop = int(x / 2)
    def f(player, roll, point, bet, total):
        strat = 'hardway-%s' % x
        if point and roll[0] == roll[1] and roll[0] == target_dietop:
            player.bankroll += bet
            player.bankroll += bet * HARDWAY_PAYOUT[total]
        if point and total == x and total in [4, 6, 8, 10]:
            player.clear_bet(strat)
        if point and total == 7:
            player.clear_bet(strat)
    return f

def pay_field(player, roll, point, bet, total):
    strat = 'field'
    if total in [2, 12]:
        player.bankroll += 3 * bet
    if total in [3, 4, 9, 10, 11]:
        player.bankroll += 2 * bet
    player.clear_bet(strat)

def pay_place_gen(num):
    def f(player, roll, point, bet, total):
        strat = 'place-%s' % num
        if point and total == num:
            player.clear_bet(strat)
            player.bankroll += bet
            player.bankroll += math.floor(bet * PLACE_PAYOUT[num])
        if point and total == 7:
            player.clear_bet(strat)
    return f

def pay_pass(player, roll, point, bet, total):
    strat = 'pass'
    total = sum(roll)
    # Losers
    if point and total == 7:
        player.clear_bet(strat)
    elif point == None and total in [2,3,12]:
        player.clear_bet(strat)
    # Winners
    elif point and total == point:
        player.bankroll += (2 * bet)
        player.clear_bet(strat)
    elif point == None and total in [7, 11]:
        player.bankroll += (2 * bet)
        player.clear_bet(strat)

def pay_dontpass(player, roll, point, bet, total):
    strat = "dontpass"
    if point and total == 7:
        player.bankroll += (2 * bet)
        player.clear_bet(strat)
    elif point == None and total in [2,3]:
        player.bankroll += (2 * bet)
        player.clear_bet(strat)
    elif point and total == point:
        player.clear_bet(strat)
    elif point == None and total in [7, 11]:
        player.clear_bet(strat)

def pay_passodds(player, roll, point, bet, total):
    strat = "passodds"
    if point and total == 7:
        player.clear_bet(strat)
    elif point and total == point:
        player.bankroll += bet
        player.bankroll += math.floor(bet * ODDS_PAYOUT[point])
        player.clear_bet(strat)

payouts = {
        'pass': pay_pass,
        'dontpass': pay_dontpass,
        'passodds': pay_passodds,
        'field': pay_field,
        'anycraps': any_craps,
        }
for i in [4, 6, 8, 10]:
    payouts['hardway-%i' % i] = hardway_gen(i)
for i in range(4, 11):
    payouts['place-%s' % i] = pay_place_gen(i)
