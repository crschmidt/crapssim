from sim import TABLE_MIN

def passline(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)

def dontline(player, point):
    if not 'dontpass' in player.current_bets and not point:
        player.bet('dontpass', TABLE_MIN)
