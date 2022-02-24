from sim import Sim, Player, TABLE_MIN

def pass_come_strat(player, point):
    if not player.current_bets.get('pass', 0) and not point:
        player.bet("pass", 15)
    if not player.current_bets.get('come') and point:
        player.bet("come", 15)

def test_pass_come_strat():
    s = Sim()
    p = Player(0, "Pass Come")
    p.set_strategy(pass_come_strat)
    s.players.append(p)
    s.rolls = [
            [3,3],
            [3,3],
            [5,6],
            [3,2],
            [3,4],
            [3,3],
            [3,4],
            [2,2],
            [5,5],
            [3,4],
        ]
    s.runsim()
if __name__ == "__main__":
    test_pass_come_strat()
