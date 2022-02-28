#!/usr/bin/python

# Copyright 2022 Christopher Schmidt
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import sim
from sim import Sim, Player
import strats.bet500 as bet500
from strats.basic import passline_amount, dontpass_amount
import csv

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sim.DEBUG = int(sys.argv[1])
    w = csv.writer(open("bet500.csv", "w"))
    outcomes = []
    header = False
    s = 0
    runs = 100000
    for i in range(runs):
        s = Sim()
        p = Player(500, "Pass $500")
        p.set_strategy(passline_amount(500))
        p.allow_overbet = False
        s.players.append(p)
        p = Player(500, "Pass/Field/Hards/Odds")
        p.set_strategy(bet500.cpg)
        p.allow_overbet = False
        s.players.append(p)
        p = Player(500, "Don't Pass $500")
        p.set_strategy(dontpass_amount(500))
        p.allow_overbet = False
        s.players.append(p)
        p = Player(500, "Don't Pass $250")
        p.set_strategy(dontpass_amount(250))
        p.allow_overbet = False
        s.players.append(p)
        p = Player(500, "Crapscheck")
        p.set_strategy(bet500.crapscheck)
        p.allow_overbet = False
        s.players.append(p)
        p = Player(500, "Hedgeless Horseman $125")
        p.set_strategy(bet500.hedgelesshorseman)
        p.allow_overbet = False
        s.players.append(p)
        p = Player(500, "Field")
        p.set_strategy(bet500.field)
        p.allow_overbet = False
        s.players.append(p)
        p = Player(500, "Field 250")
        p.set_strategy(bet500.field250)
        p.allow_overbet = False
        s.players.append(p)
        if not header:
            w.writerow([p.name for p in s.players])
            for i in s.players:
                outcomes.append([])
            header = True
#        p.set_strategy(bet500.cpg)
        # startgame
        s.singleroll()
        while not s.new_shooter:
            s.singleroll()
#        print "Run #%s: %s" % (i, p.bankroll)
        o = []
        for i in range(len(s.players)):
            p = s.players[i]
            outcome = p.bankroll - max(500-p.total_bet_amount, 0)
    #    print "Outcome: %s (Total bets: %s, bankroll: %s)" % (outcome, p.total_bet_amount, p.bankroll)
            outcomes[i].append(outcome)
            o.append(outcome)
        w.writerow(o)
    for i in range(len(s.players)):
        o = outcomes[i]

        print("%s: Average: $%s; Broke: %.2f%%; Equal or better: %.2f%%; Triple: %.2f%%" % (s.players[i].name, sum(o)/len(o), 100.0*len(filter(lambda x: x == 0, o))/runs, 100.0*len(filter(lambda x: x >= 500, o))/runs, 100.0*len(filter(lambda x: x >= 1500, o))/runs))
