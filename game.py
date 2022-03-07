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
from strats.basic import passline, dontline, passline_amount, always_field, always_hards, any_craps
import strats.odds
from strats.always_come import pass_come_strat
from strats.hedgelesshorseman import hedgelesshorseman
from strats.dodont import dodont, dontdo
from strats.colorup import conservative_15, darkside_hedge
import strats.place
import strats.testing
from rolls.colorup import casinoquest_hedge, conservative

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sim.DEBUG = int(sys.argv[1])
    s = Sim()
#    s.rolls = conservative
    p = Player(0, "Pass")
    p.set_strategy(passline)
    s.players.append(p)
    p = Player(0, "DP/Hard")
    p.set_strategy(strats.testing.mix_30)
    s.players.append(p)
    p = Player(0, "DP/Place")
    p.set_strategy(strats.testing.dp_place)
    s.players.append(p)
    p = Player(0, "DP/Lay")
    p.set_strategy(strats.testing.lay_place)
    s.players.append(p)
    p = Player(0, "Darkside Hedge")
    p.set_strategy(darkside_hedge)
    s.players.append(p)
#    p = Player(0, "Craps")
#    p.set_strategy(any_craps)
#    s.players.append(p)
#    p = Player(0, "Hards")
#    p.set_strategy(always_hards)
#    s.players.append(p)
#    p = Player(0, "Place 6/8")
#    p.set_strategy(strats.place.place_6_8)
#    s.players.append(p)
#    p = Player(0, "Place Inside")
#    p.set_strategy(strats.place.place_inside)
#    s.players.append(p)
#    p = Player(0, "Field only")
#    p.set_strategy(always_field)
#    s.players.append(p)
    p = Player(0, "Conservative 15")
    p.set_strategy(conservative_15)
    s.players.append(p)

#    p = Player(0, "Don't Pass")
#    p.set_strategy(dontline)
#    s.players.append(p)
#    p = Player(0, "$25 Pass/$15 Don't")
#    p.set_strategy(dodont)
#    s.players.append(p)
#    p = Player(0, "$25 Don't/$15 Pass")
#    p.set_strategy(dontdo)
#    s.players.append(p)
#    p = Player(0, "Pass 5x 6/8")
#    p.set_strategy(strats.odds.pass_5x_6_8)
#    s.players.append(p)
#    p = Player(0, "Allpoint Molly")
#    p.set_strategy(pass_come_strat)
#    s.players.append(p)
    s.rollcount = 5000
    s.runsim()
