import sys
import sim
from sim import Sim, Player
from strats.basic import passline, dontline
import strats.odds
from strats.always_come import pass_come_strat
from strats.hedgelesshorseman import hedgelesshorseman

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sim.DEBUG = int(sys.argv[1])
    s = Sim()
    p = Player(0, "Pass")
    p.set_strategy(passline)
    s.players.append(p)
    p = Player(0, "Dont")
    p.set_strategy(dontline)
    s.players.append(p)
    p = Player(0, "Pass 100x")
    p.set_strategy(strats.odds.pass_100x)
    s.players.append(p)
    p = Player(0, "Pass 10x")
    p.set_strategy(strats.odds.pass_10x)
    s.players.append(p)
    p = Player(0, "Pass 5x")
    p.set_strategy(strats.odds.pass_5x)
    s.players.append(p)
    p = Player(0, "Pass 5x 6/8")
    p.set_strategy(strats.odds.pass_5x_6_8)
    s.players.append(p)
    p = Player(0, "Pass Come")
    p.set_strategy(pass_come_strat)
    s.players.append(p)
    p = Player(0, "Hedgeless")
    p.set_strategy(hedgelesshorseman)
    s.players.append(p)
    s.rollcount = 5000
    s.runsim()
