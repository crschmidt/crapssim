from sim import TABLE_MIN

def place_6_8(player, point):
    if not 'place-6' in player.current_bets:
        player.bet('place-6', 18)
    if not 'place-8' in player.current_bets:
        player.bet('place-8', 18)

def place_inside(player, point):
    for i in [6, 8]:
        if not 'place-%s' % i in player.current_bets:
            player.bet('place-%s' % i, 18)
    for i in [5, 10]:
        if not 'place-%s' % i in player.current_bets:
            player.bet('place-%s' % i, 15)
