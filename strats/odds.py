from sim import TABLE_MIN

def pass_100x(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point:
        player.bet('passodds', 100*TABLE_MIN)

def pass_10x(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point:
        player.bet('passodds', 10*TABLE_MIN)

def pass_5x(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point:
        player.bet('passodds', 5*TABLE_MIN)

def pass_5x_6_8(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point in [6, 8]:
        player.bet('passodds', 5*TABLE_MIN)
