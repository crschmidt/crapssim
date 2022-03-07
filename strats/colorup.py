def conservative_15(player, point, new_shooter=False):
    if new_shooter:
        player.strat_status={'placewins': 0, 'placed': False}
    if point:
        if not player.current_bets.get('lay-4', 0):
            player.bet('lay-4', 40)
        if player.strat_status['placed']:
            if not player.current_bets.get('place-6',0):
                player.strat_status['placewins'] += 1
                player.bet('place-6', 18)
            if not player.current_bets.get('place-8',0):
                player.strat_status['placewins'] += 1
                player.bet('place-8', 18)
        else:
            player.strat_status['placed'] = True
            player.bet('place-6', 18)
            player.bet('place-8', 18)
    if player.strat_status['placewins'] >= 2:
        player.unbet('place-6')
        player.unbet('place-8')

# How Math Teacher Wins at Casino Craps"
def darkside_hedge(player, point, new_shooter=False):
#    if not point:
#        if not 'horn-12' in player.current_bets:
#            player.bet('horn-12', 1)
    if not 'dontpass' in player.current_bets:
        player.bet('dontpass', 15)
    for i in ['lay-4', 'lay-10']:
        if not i in player.current_bets:
            player.bet(i, 40)

