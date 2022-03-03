from sim import Sim, Player
from strats.basic import passline
from strats.hedgelesshorseman import hedgelesshorseman
from strats.basic import passline, dontline, passline_amount, always_field, always_hards, any_craps
from strats.odds import pass_5x_6_8
from strats.colorup import conservative_15
import strats.testing

broke = 0
double = 0
positive = 0
negative = 0
START = 500 

RUNS=10000

import csv
w = csv.writer(open("out.csv", "w"))

for i in range(RUNS):
    s = Sim()
    p = Player(0, "Pass")
    p.set_strategy(passline)
    s.players.append(p)
    for j in range(250):
        s.singleroll()
        if s.players[0].bankroll < -START:
            broke += 1
#            print broke, double
            break
        if s.players[0].bankroll > START:
            double += 1
#            print broke, double
            break
    w.writerow([s.players[0].bankroll])
    if s.players[0].bankroll > 0:
        positive += 1
    else:
        negative += 1
    if i % 1000 == 0: print "Run #%s complete" % i
print "Go broke: %s%%, Double money: %s%%; Positive: %s, Negative: %s" % (100.0*broke/RUNS, 100*double/RUNS, positive, negative)
