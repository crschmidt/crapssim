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
from strats.basic import passline, dontline, passline_amount
import strats.odds
from strats.always_come import pass_come_strat
from strats.hedgelesshorseman import hedgelesshorseman
from strats.dodont import dodont, dontdo
from rolls.colorup import casinoquest_hedge

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sim.DEBUG = int(sys.argv[1])
    s = Sim()
   # s.rolls = casinoquest_hedge
    p = Player(0, "Pass")
    p.set_strategy(passline)
    s.players.append(p)
    p = Player(0, "Don't Pass")
    p.set_strategy(dontline)
    s.players.append(p)
    p = Player(0, "$25 Pass/$15 Don't")
    p.set_strategy(dodont)
    s.players.append(p)
    p = Player(0, "$25 Don't/$15 Pass")
    p.set_strategy(dontdo)
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
    s.rollcount = 2500
    s.runsim()
