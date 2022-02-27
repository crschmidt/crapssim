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

def passline_amount(amount):
    def f(player, point):
        if not 'pass' in player.current_bets and not point:
            player.bet('pass', amount)
    return f

def passline(player, point):
    if not 'pass' in player.current_bets and not point:
        player.bet('pass', TABLE_MIN)

def dontline(player, point):
    if not 'dontpass' in player.current_bets and not point:
        player.bet('dontpass', TABLE_MIN)

def dontpass_amount(amount):
    def f(player, point):
        if not 'dontpass' in player.current_bets and not point:
            player.bet('dontpass', amount)
    return f

def always_field(player, point):
    if not 'field' in player.current_bets:
        player.bet('field', TABLE_MIN)

def always_hards(player, point):
    for i in [4, 6, 8, 10]:
        if not ('hardway-%s' % i) in player.current_bets:
            player.bet('hardway-%s' % i, 1)

def any_craps(player, point):
    if not player.current_bets.get("anycraps", 0):
        player.bet('anycraps', 1)
