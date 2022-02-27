ODDS_PAYOUT = {4: 2.0, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2.0}


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
