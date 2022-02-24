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

def hedgelesshorseman(player, point):
    # Never put out more than 4 bets.
    if sum(player.current_bets.values()) >= 100: return
    if not player.current_bets.get('dontpass', 0) and not point:
        player.bet("dontpass", 25)
    if not player.current_bets.get('come') and point:
        player.bet("come", 25)

def test_pass_come_strat():
    s = Sim()
    p = Player(600, "Hedgeless")
    p.set_strategy(hedgelesshorseman)
    s.players.append(p)
    s.rolls = [
            [5, 5],
            [4, 2],
            [5, 3],
            [5, 6],
            [5, 1],
            [6, 2],
            [3, 1],
            [4, 3],
            [5, 1],
            [2, 1],
            [5, 1],
            [3, 3],
            [2, 1],
            [3, 2],
            [6, 2],
            [5, 4],
        ]
    s.runsim()
    assert (p.bankroll + sum(p.current_bets.values()) == 575)
if __name__ == "__main__": 
    test_pass_come_strat()
