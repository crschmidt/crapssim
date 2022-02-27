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

from bets import *

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

ODDS_PAYOUT = {4: 2.0, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2.0}

payouts = {
        'pass': pay_pass,
        'dontpass': pay_dontpass,
        'passoddds': pay_passodds,
        }


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
        w2 = csv.writer(open("edge.csv", "w"))
        w2.writerow(["rollnum", "point", "total"] + map(lambda x: x.name, self.players))
        w = csv.writer(open("out.csv", "w"))
        w.writerow(["rollnum", "point", "total"] + map(lambda x: x.name, self.players))
        shooter_output = csv.writer(open("shooters.csv", "w"))
        shooter_output.writerow(["rollnum", "point", "total"] + map(lambda x: x.name, self.players))
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
        new_shooter = True
        while n < self.rollcount:
            n += 1
            if n % 10000 == 0: print "Roll #%s" % n
            r = self.roll()
            if len(r) == 0:
                debug("Out of rolls")
                break
            if new_shooter == True:
                for p in self.players:
                    p.shooter_start = p.bankroll
                new_shooter = False
            for p in self.players:
                p.apply_strat(point)
                debug(" == %s == Bets: %s" % (p.name, p.current_bets), 2)
            total = sum(r)
            debug("Point is %s, Roll is %s (%s); paying players" % (point, total, r))
            for p in self.players:
                payout(p, r, point)

            out = [n, point, total]
            out2 = [n, point, total]
            shooter_status = [n, point, total]
            if point and total == 7:
                debug("Seven out")
                point = None
                shooters += 1
                seven_out += 1
                new_shooter = True
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
            for i in self.players:
                out2.append("%.2f" % (100.0*i.delta()/i.total_bet_amount))
            if new_shooter:
                for i in self.players:
                    shooter_status.append(i.bankroll - i.shooter_start)
                shooter_output.writerow(shooter_status)
            w.writerow(out)
            w2.writerow(out2)

        print "Rolls: %s, Shooters: %s, Points Met: %s, Come winner: %s, Come Craps: %s, Seven out: %s" % (n, shooters, points, come_winner, come_loser, seven_out)
        for p in self.players:
            print "Strategy: %s; End bankroll: %s, Delta: %.3f%%" % (p.name, p.money(), (100.0*p.delta()/p.total_bet_amount))
        return n
