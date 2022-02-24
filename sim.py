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

import csv
import random
import math


TABLE_MIN = 15

DEBUG = 0 

def debug(s, level=1):
    if DEBUG:
        if level <= DEBUG:
            print s

class Player():
    bankroll = 0
    total_bets = 0
    total_bet_amount = 0
    current_bets = None
    name = "Player"
    def __init__(self, bankroll = 0, name="Player"):
        self.current_bets = {}
        self.bankroll = self.starting_bankroll = bankroll
        self.name = name
    def clear_bet(self, t):
        del self.current_bets[t]
    def bet(self, t, amount):
        self.current_bets[t] = self.current_bets.get(t, 0)+amount
        self.bankroll -= amount
        self.total_bet_amount += amount
        self.total_bets += 1
    def set_strategy(self, f):
        self.strategy = f
    def apply_strat(self, point):
        self.strategy(self, point)
    def money(self, onthetable=True):
        return self.bankroll + sum(self.current_bets.values())
    def delta(self):
        return self.money() - self.starting_bankroll


def dual_reverse_strat(player, point):
    if not player.current_bets('pass', 0): 
        player.bet('pass', TABLE_MIN)

        player.current_bets['pass'] = (TABLE_MIN)
        player.bankroll -= (TABLE_MIN)
        player.total_bets += 1
        player.total_bet_amount += (TABLE_MIN)

    if not 'dontpass' in player.current_bets or player.current_bets['dontpass'] == 0:
        player.current_bets['dontpass'] = (TABLE_MIN+10)
        player.bankroll -= (TABLE_MIN+10)
        player.total_bets += 1
        player.total_bet_amount += (TABLE_MIN+10)

def dual_strat(player, point):
    if not 'pass' in player.current_bets or player.current_bets['pass'] == 0:
        player.current_bets['pass'] = (TABLE_MIN + 10)
        player.bankroll -= (TABLE_MIN + 10)
        player.total_bets += 1
        player.total_bet_amount += (TABLE_MIN + 10)

    if not 'dontpass' in player.current_bets or player.current_bets['dontpass'] == 0:
        player.current_bets['dontpass'] = TABLE_MIN
        player.bankroll -= TABLE_MIN
        player.total_bets += 1
        player.total_bet_amount += TABLE_MIN

def pass_strat_40(player, point):
    if not 'pass' in player.current_bets or player.current_bets['pass'] == 0:
        player.current_bets['pass'] = 40
        player.bankroll -= 40
        player.total_bets += 1
        player.total_bet_amount += 40

def pass_strat_10(player, point):
    if not 'pass' in player.current_bets or player.current_bets['pass'] == 0:
        player.current_bets['pass'] = 10
        player.bankroll -= 10
        player.total_bets += 1
        player.total_bet_amount += 10

def pass_strat_25(player, point):
    if not 'pass' in player.current_bets or player.current_bets['pass'] == 0:
        player.current_bets['pass'] = 25
        player.bankroll -= 25
        player.total_bets += 1
        player.total_bet_amount += 25

def pass_center_odds_strat(player, point):
    pass_strat(player, point)
    if not 'passodds' in player.current_bets or player.current_bets['passodds'] == 0:
#        print "Betting %s" % TABLE_MIN
        if point in [6,8]:
            bet = TABLE_MIN
            player.current_bets['passodds'] = bet
            player.bankroll -= bet
            player.total_bets += 1
            player.total_bet_amount += bet

def pass_1x_odds_strat(player, point):
    pass_strat(player, point)
#    print "Pass: %s, %s" % (player.name, player.bankroll)
    if not 'passodds' in player.current_bets or player.current_bets['passodds'] == 0:
#        print "Betting %s" % TABLE_MIN
        bet = TABLE_MIN
        player.current_bets['passodds'] = bet
        player.bankroll -= bet
        player.total_bets += 1
        player.total_bet_amount += bet

def pass_odds_strat(player, point):
    pass_strat(player, point)
#    print "Pass: %s, %s" % (player.name, player.bankroll)
    if not 'passodds' in player.current_bets or player.current_bets['passodds'] == 0:
#        print "Betting %s" % TABLE_MIN
        bet = 3 * TABLE_MIN
        player.current_bets['passodds'] = bet
        player.bankroll -= bet
        player.total_bets += 1
        player.total_bet_amount += bet

ODDS_PAYOUT = {4: 2.0, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2.0}

def payout(player, roll, point):
    total = sum(roll)
    prev_bank = player.bankroll
    if 'pass' in player.current_bets:
        strat = 'pass'
        bet = player.current_bets['pass']
        # Losers
        if point and total == 7:
            player.clear_bet(strat)
        elif point == None and total in [2,3,12]:
            player.clear_bet(strat)
        # Winners
        elif point and total == point:
            player.bankroll += (2 * bet)
            player.clear_bet(strat)
        elif point == None and total in [7, 11]:
            player.bankroll += (2 * bet)
            player.clear_bet(strat)
    
    if "dontpass" in player.current_bets:
        strat = "dontpass"
        bet = player.current_bets[strat]
        if point and total == 7:
            player.bankroll += (2 * bet)
            player.clear_bet(strat)
        elif point == None and total in [2,3]:
            player.bankroll += (2 * bet)
            player.clear_bet(strat)
        elif point and total == point:
            player.clear_bet(strat)
        elif point == None and total in [7, 11]:
            player.clear_bet(strat)

    if "passodds" in player.current_bets:
        strat = "passodds"
        bet = player.current_bets[strat]
        if point and total == 7:
            player.clear_bet(strat)
        elif point and total == point:
            player.bankroll += bet
            player.bankroll += math.floor(bet * ODDS_PAYOUT[point])
            player.clear_bet(strat)
    
    # Need to pay come bets *before* moving the come up
    for i in [4, 5, 6, 8, 9, 10]:
        strat = "come-%s" % i
        if player.current_bets.get(strat, 0):
            bet = player.current_bets[strat]
            if total == 7:
                player.clear_bet(strat)
            elif total == i:
                player.clear_bet(strat)
                player.bankroll += 2 * bet
        strat = "come-odds-%s" % i
        if player.current_bets.get(strat, 0):
            bet = player.current_bets[strat]
            if total == 7:
                player.clear_bet(strat)
            elif total == i:
                player.clear_bet(strat)
                player.bankroll += bet
                player.bankroll += math.floor(bet * ODDS_PAYOUT[total])

    if "come" in player.current_bets and player.current_bets["come"] != 0:
        strat = "come"
        bet = player.current_bets[strat]
        if point:
            if total in [7, 11]:
                player.clear_bet(strat)
                player.bankroll += (2 * bet)
            elif total in [2,3,12]:
                player.clear_bet(strat)
            else:
                player.clear_bet(strat)
                s = "come-%s" % total
                player.current_bets[s] = bet



class Sim():
    players = None
    rolls = None
    rollcount = 100

    def __init__(self):
        self.players = []

    def roll(self):
        if self.rolls != None:
            if len(self.rolls):
                return self.rolls.pop(0)
            return []
        return [random.randint(1,6), random.randint(1,6)]

    def run(self):
        rolls = []
        while len(rolls) < 1000000:
            rolls.append(self.runsim())
        print "Total rolls before broke: %s" % rolls
        print "Broke in under an hour: %s" % len(filter(lambda x: x < 120, rolls))
        print "Worst: %s; Best: %s; Average: %s" % (min(rolls), max(rolls), float(sum(rolls))/len(rolls))

    def runsim(self):
        w = csv.writer(open("out.csv", "w"))
        w.writerow(["rollnum", "point", "total"] + map(lambda x: x.name, self.players))
        point = None
        n = 0
        shooters = 1
        points = 0
        come_winner = 0
        come_loser = 0
        seven_out = 0
        deltas = []
        bankrolls = []
        status = 0
        while n < self.rollcount:
            n += 1
            if n % 10000 == 0: print "Roll #%s" % n
            r = self.roll()
            if len(r) == 0:
                debug("Out of rolls")
                break
            for p in self.players:
                p.apply_strat(point)
                debug(" == %s == Bets: %s" % (p.name, p.current_bets), 2)
            total = sum(r)
            debug("Point is %s, Roll is %s (%s); paying players" % (point, total, r))
            for p in self.players:
                payout(p, r, point)

            out = [n, point, total]
            if point and total == 7:
                debug("Seven out")
                point = None
                shooters += 1
                seven_out += 1
            elif point and total == point:
                debug("Point met")
                point = None
                points += 1
            elif point == None and total in [7, 11]:
                debug("Winner")
                come_winner += 1
            elif point == None and total in [2, 3, 12]:
                debug("Loser")
                come_loser += 1
            elif point == None:
                debug("Point is %s" % total)
                point = total
            status = points + come_winner - come_loser - seven_out
            for p in self.players:
                debug("%s: %s" % (p.name, p.money()))
            deltas.append(status)
            for i in self.players:
                out.append(i.bankroll)

            w.writerow(out)

        print "Rolls: %s, Shooters: %s, Points Met: %s, Come winner: %s, Come Craps: %s, Seven out: %s" % (n, shooters, points, come_winner, come_loser, seven_out)
        for p in self.players:
            print "Strategy: %s; End bankroll: %s, Delta: %.3f%%" % (p.name, p.money(), (100.0*p.delta()/p.total_bet_amount))
        return n
