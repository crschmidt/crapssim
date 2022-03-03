def dp_place(player, point):
    if not point:
        player.bet("dontpass", 50)
    if point:
        for i in [4, 5, 6, 8, 9, 10]:
            if i == point:
                continue
            if not player.current_bets.get("point-%s" % i, 0):
                if i in [6, 8]:
                    player.bet("place-%s" % i, 12)
                else:
                    player.bet("place-%s" % i, 10)


def lay_place(player, point):
    if not "lay-4" in player.current_bets:
        player.bet("lay-4", 100)
    if point:
        for i in [5, 6, 8, 9, 10]:
            if not player.current_bets.get("point-%s" % i, 0):
                if i in [6, 8]:
                    player.bet("place-%s" % i, 12)
                else:
                    player.bet("place-%s" % i, 10)

def mix_30(player, point):
    if not point and not 'dontpass' in player.current_bets:
        player.bet("dontpass", 30)
    if not point:
        for i in ['hardway-4', 'hardway-10', 'place-6', 'place-8']:
            if i in player.current_bets:
                player.unbet(i)
    if point:
        for i in [6, 8]:
            if i == point: continue
            s = "place-%s" % i
            if not s in player.current_bets:
                player.bet(s, 30)
        for i in [4, 10]:
            if point==i:
                if not 'hardway-%s' % i in player.current_bets:
                    player.bet("hardway-%s" % i, 5)
