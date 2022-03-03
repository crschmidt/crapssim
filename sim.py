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

from bets import payouts

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
    min_rack = 0
    allow_overbet = True
    strat_status = None

    def __init__(self, bankroll = 0, name="Player"):
        self.current_bets = {}
        self.strat_status = {}
        self.bankroll = self.starting_bankroll = bankroll
        self.name = name
    def clear_bet(self, t):
        del self.current_bets[t]
    def unbet(self, t):
        if t in 'pass' or t.startswith("come-"): return
        if not t in self.current_bets: return
        bet = self.current_bets.get(t, 0)
        self.bankroll += bet
        del self.current_bets[t]
        
    def bet(self, t, amount):
        if t not in payouts:
            raise Exception("%s not a valid bet" % t)
        if self.allow_overbet != True and amount > self.bankroll:
            debug("Attempted overbet %s on bankroll of %s" % (amount, self.bankroll), 1)
            return
        self.current_bets[t] = self.current_bets.get(t, 0)+amount
        self.bankroll -= amount
        self.total_bet_amount += amount
        self.total_bets += 1
        if self.bankroll < self.min_rack:
            self.min_rack = self.bankroll
    def set_strategy(self, f):
        self.strategy = f
    def apply_strat(self, point, new_shooter=False):
        try:
            self.strategy(self, point, new_shooter)
        except Exception, E:
            self.strategy(self, point)
    def money(self, onthetable=True):
        return self.bankroll + sum(self.current_bets.values())
    def delta(self):
        return self.money() - self.starting_bankroll

ODDS_PAYOUT = {4: 2.0, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2.0}


def payout(player, roll, point):
    total = sum(roll)
    prev_bank = player.bankroll
    for strat in payouts:
        if player.current_bets.get(strat, 0) > 0:
            bet = player.current_bets[strat]
            payouts[strat](player, roll, point, bet, total)

    # Need to pay come bets *before* moving the come up
    for i in [4, 5, 6, 8, 9, 10]:
        strat = "dontcome-%s" % i
        if player.current_bets.get(strat, 0):
            bet = player.current_bets[strat]
            if total == 7:
                player.clear_bet(strat)
                player.bankroll += 2 * bet
            elif total == i:
                player.clear_bet(strat)
        strat = "dontcome-odds-%s" % i
        if player.current_bets.get(strat, 0):
            bet = player.current_bets[strat]
            if total == 7:
                player.bankroll += bet
                player.bankroll += math.floor(bet * ODDS_PAYOUT[total])
                player.clear_bet(strat)
            elif total == i:
                player.clear_bet(strat)

    if player.current_bets.get("dontcome", 0):
        strat = "dontcome"
        bet = player.current_bets[strat]
        if point:
            if total in [7, 11]:
                player.clear_bet(strat)
            elif total in [2,3]:
                player.bankroll += (2 * bet)
                player.clear_bet(strat)
            else:
                # Move the bet up
                player.clear_bet(strat)
                s = "dontcome-%s" % total
                player.current_bets[s] = bet
    
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
                # Move the bet up
                player.clear_bet(strat)
                s = "come-%s" % total
                player.current_bets[s] = bet

class Sim():
    players = None
    rolls = None
    rollcount = 100
    outcomes = None
    point = None
    new_shooter = True
    rollnum = 0

    def __init__(self):
        self.players = []
        self.writers = {
                'edge': csv.writer(open('edge.csv', 'w')),
                'roll': csv.writer(open('roll.csv', 'w')),
                'shooter': csv.writer(open('shooter.csv', 'w')),
            }
        self.outcomes = {
                'shooters': 0,
                'points': 0,
                'comeout_winner': 0,
                'comeout_loser': 0,
                'seven_out': 0,
            }

    def outcome(self, name):
        debug(name)
        self.outcomes[name] += 1

    def rolldice(self):
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

    def write_header(self):
        for v in self.writers.values():
            v.writerow(["rollnum", "point", "total"] + map(lambda x: x.name, self.players))

    def write(self, roll_status, new_shooter=False):
        roll = roll_status[:]
        for i in self.players:
            roll.append(i.bankroll)
        self.writers['roll'].writerow(roll)
        if new_shooter:
            edge = roll_status[:]
            shooter = roll_status[:]
            for i in self.players:
                edge.append("%.2f" % (100.0*i.delta()/i.total_bet_amount))
                shooter.append(i.bankroll - i.shooter_start)
            self.writers['shooter'].writerow(shooter)
            self.writers['edge'].writerow(edge)

    def singleroll(self):
        self.rollnum += 1
        if self.rollnum % 10000 == 0: print "Roll #%s" % self.rollnum
        r = self.rolldice()
        if len(r) == 0:
            debug("Out of rolls")
            return True
        ns = self.new_shooter
        if self.new_shooter == True:
            for p in self.players:
                p.shooter_start = p.bankroll
            self.new_shooter = False
            self.outcome('shooters')
        for p in self.players:
            p.apply_strat(self.point, ns)
            debug(" == %s == Bets: %s" % (p.name, p.current_bets), 2)
        total = sum(r)
        debug("Point is %s, Roll is %s (%s); paying players" % (self.point, total, r))
        for p in self.players:
            payout(p, r, self.point)

        roll_status = [self.rollnum, self.point, total]
        if self.point and total == 7:
            self.outcome('seven_out')
            self.point = None
            self.new_shooter = True
        elif self.point and total == self.point:
            self.outcome('points')
            self.point = None
        elif self.point == None and total in [7, 11]:
            self.outcome('comeout_winner')
        elif self.point == None and total in [2, 3, 12]:
            self.outcome('comeout_loser')
        elif self.point == None:
            debug("Point is %s" % total)
            self.point = total
        for p in self.players:
            debug("%s: %s" % (p.name, p.money()))
        self.write(roll_status, self.new_shooter)

    def runsim(self):
        self.write_header()
        stop = False
        while self.rollnum < self.rollcount and not stop:
            stop = self.singleroll()

        print "Rolls: %s, Shooters: %s, Points Met: %s, Come winner: %s, Come Craps: %s, Seven out: %s" % (self.rollnum, self.outcomes['shooters'], self.outcomes['points'], self.outcomes['comeout_winner'], self.outcomes['comeout_loser'], self.outcomes['seven_out'])
        for p in self.players:
            print "Strategy: %s; End bankroll: %s, Delta: %.3f%% (min rack: %s)" % (p.name, p.money(), (100.0*p.delta()/p.total_bet_amount), p.min_rack)
