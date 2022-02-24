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
