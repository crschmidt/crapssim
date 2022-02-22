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

DEBUG = False #True

def debug(s):
    if DEBUG == True:
        print s

class Player():
    bankroll = 0
    total_bets = 0
    total_bet_amount = 0
    current_bets = None
    name = "Player"
    def __init__(self, bankroll = 0, name="Player"):
        self.current_bets = {}
        self.bankroll = bankroll
        self.name = name
    def bet(t, amount):
        self.current_bets[t] = amount

    def set_strategy(self, f):
        self.strategy = f
    def apply_strat(self, point):
        self.strategy(self, point)

def dual_reverse_strat(player, point):
    if not 'pass' in player.current_bets or player.current_bets['pass'] == 0:
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
#    print "Pass: %s, %s" % (player.name, player.bankroll)
    if not 'pass' in player.current_bets or player.current_bets['pass'] == 0:
#        print "Betting %s" % TABLE_MIN
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

def pass_strat(player, point):
#    print "Pass: %s, %s" % (player.name, player.bankroll)
    if not 'pass' in player.current_bets or player.current_bets['pass'] == 0:
#        print "Betting %s" % TABLE_MIN
        player.current_bets['pass'] = TABLE_MIN
        player.bankroll -= TABLE_MIN
        player.total_bets += 1
        player.total_bet_amount += TABLE_MIN

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

def dontpass_strat(player, point):
#    print "Don't Pass: %s, %s" % (player.name, player.bankroll)
    if not 'dontpass' in player.current_bets or player.current_bets['dontpass'] == 0:
#        print "Betting %s" % TABLE_MIN
        player.current_bets['dontpass'] = TABLE_MIN
        player.bankroll -= TABLE_MIN
        player.total_bets += 1
        player.total_bet_amount += TABLE_MIN

ODDS_PAYOUT = {4: 2.0, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2.0}

def payout(player, roll, point):
#    print player.name
    total = sum(roll)
    prev_bank = player.bankroll
    if 'pass' in player.current_bets:
        bet = player.current_bets['pass']
        # Losers
        if point and total == 7:
            player.current_bets['pass'] = 0
        elif point == None and total in [2,3,12]:
            player.current_bets['pass'] = 0
        # Winners
        elif point and total == point:
            player.bankroll += (2 * bet)
            player.current_bets['pass'] = 0
        elif point == None and total in [7, 11]:
#            print "PAYOUT: Come out winner, %s" % player.bankroll
            player.bankroll += (2 * bet)
            player.current_bets['pass'] = 0
#            print "PAYOUT2: Come out winner, %s" % player.bankroll
    if "dontpass" in player.current_bets:
        strat = "dontpass"
        bet = player.current_bets[strat]
        if point and total == 7:
            player.bankroll += (2 * bet)
            player.current_bets[strat] = 0
        elif point == None and total in [2,3]:
            player.bankroll += (2 * bet)
            player.current_bets[strat] = 0
        elif point and total == point:
            player.current_bets[strat] = 0
        elif point == None and total in [7, 11]:
            player.current_bets[strat] = 0

    if "passodds" in player.current_bets:
        strat = "passodds"
        bet = player.current_bets[strat]
        if point and total == 7:
            player.current_bets['passodds'] = 0
        elif point and total == point:
            player.bankroll += bet
            player.bankroll += math.floor(bet * ODDS_PAYOUT[point])

            player.current_bets['passodds'] = 0

#    print player.current_bets
    debug("%s Winnings: %s" % (player.name, (player.bankroll - prev_bank)))


class Sim():

    players = []

    def roll(self):
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
        while n < 10000:
            for p in self.players:
                p.apply_strat(point)
#        while status > -10:
            n += 1
            r = self.roll()
            for p in self.players:
                payout(p, r, point)
            total = sum(r)

            out = [n, point, total]
            debug("Point is %s, Roll is %s (%s)" % (point, total, r))
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
                debug("%s: %s" % (p.name, p.bankroll))
            deltas.append(status)
            for i in self.players:
                out.append(i.bankroll)

            w.writerow(out)

#            bankrolls.append(self.players[0].bankroll)
    #    print n
        print "Rolls: %s, Shooters: %s, Points Met: %s, Come winner: %s, Come Craps: %s, Seven out: %s" % (n, shooters, points, come_winner, come_loser, seven_out)
#        print bankrolls
#        print deltas
        print status
    #    print max(deltas), min(deltas)
        for p in self.players:
            print "Strategy: %s; End bankroll: %s, Delta: %.3f%%" % (p.name, p.bankroll, (100.0*p.bankroll/p.total_bet_amount))
        return n
        


if __name__ == "__main__":
    s = Sim()
    #p = Player(0, "Pass 10")
    #p.set_strategy(pass_strat_10)
    #s.players.append(p)
    p = Player(0, "Pass 15")
    p.set_strategy(pass_strat)
    s.players.append(p)
    #p = Player(0, "Pass 25")
    #p.set_strategy(pass_strat_25)
    #s.players.append(p)
    #p = Player(0, "Pass 40")
    #p.set_strategy(pass_strat_40)
    #s.players.append(p)
    p = Player(0, "Pass 15 Odds")
    p.set_strategy(pass_odds_strat)
    s.players.append(p)
    p = Player(0, "Don't Pass")
    p.set_strategy(dontpass_strat)
    s.players.append(p)
    p = Player(0, "Pass 15 1x Odds")
    p.set_strategy(pass_1x_odds_strat)
    s.players.append(p)
    p = Player(0, "Pass 15 1x Inner Odds")
    p.set_strategy(pass_center_odds_strat)
    s.players.append(p)

    #p = Player(0, "25 pass / 15 dp")
    #p.set_strategy(dual_strat)
    #s.players.append(p)
    #p = Player(0, "25 dp / 15 pass")
    #p.set_strategy(dual_reverse_strat)
    #s.players.append(p)
    s.runsim()
