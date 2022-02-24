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

from sim import TABLE_MIN

def pass_100x(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point:
        player.bet('passodds', 100*TABLE_MIN)

def pass_10x(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point:
        player.bet('passodds', 10*TABLE_MIN)

def pass_5x(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point:
        player.bet('passodds', 5*TABLE_MIN)

def pass_5x_6_8(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)
    if not 'passodds' in player.current_bets and point in [6, 8]:
        player.bet('passodds', 5*TABLE_MIN)
