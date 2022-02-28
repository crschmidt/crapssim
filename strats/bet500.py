def cpg(player, point):
    if player.bankroll > 1500:
        for i in list(player.current_bets.keys()):
            player.unbet(i)
        return
    if point:
        bet_if_empty(player, "passodds", 200)
    if not point:
        for i in [4, 6, 8, 10]:
            bet_if_empty(player, "hard-%s" % i, 25)
        bet_if_empty(player, "pass", 100)
    player.bet("field", 100)

def bet_if_empty(player, strat, amount):
    if player.current_bets.get(strat, 0) == 0:
        player.bet(strat, amount)

def field(player, point):
    player.bet("field", 500)
def field250(player, point):
    player.bet("field", 250)

def crapscheck(player, point):
    if not point:
        player.bet("anycraps", 100)
        bet_if_empty(player, "pass", min(400, player.bankroll))

def hedgelesshorseman(player, point):
    # Never put out more than 4 bets.
    if sum(player.current_bets.values()) >= 500: return
    if not player.current_bets.get('dontpass', 0) and not point:
        player.bet("dontpass", 125)
    if not player.current_bets.get('come') and point:
        player.bet("come", 125)
