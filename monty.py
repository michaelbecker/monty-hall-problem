#!/usr/bin/python3
#############################################################################
#
# Test various combinations of the Monty Hall Problem.
# see: https://en.wikipedia.org/wiki/Monty_Hall_problem
#
# MIT License
# 
# Copyright (c) 2016, Michael Becker (michael.f.becker@gmail.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT 
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
#############################################################################
"""
Test various combinations of the Monty Hall Problem.
    https://en.wikipedia.org/wiki/Monty_Hall_problem
"""
import random
import sys

# Do this at the start, we are going to use this module a lot.
random.seed();

total_games = 100000
games_run = 0
total_wins = 0


def create_stage():
    """Create the initial game"""
    car_index = random.randrange(3)
    stage = [0, 0, 0]
    stage[car_index] = 1
    return stage;


def contestant_wins(stage, contestant_pick):
    """Returns True if the contestant wins, False otherwise."""
    if stage[contestant_pick] == 1:
        return True
    else:
        return False


def run_simple_game():
    """A default game, contestant picks and wins or not."""
    stage = create_stage()
    contestant_pick = random.randrange(3)
    wins = contestant_wins(stage, contestant_pick)
    return wins


def monty_pick_first_possible(stage, contestant_pick):
    """Monty picks the first possbile goat."""
    if stage[0] == 0 and contestant_pick != 0:
        stage[0] = -1
        return 0
    elif stage[1] == 0 and contestant_pick != 1:
        stage[1] = -1
        return 1
    else:
        stage[2] = -1
        return 2


def monty_pick_random(stage, contestant_pick):
    """Monty picks a random goat, if possible."""
    while True:
        pick = random.randrange(3)
        if pick == contestant_pick:
            continue
        elif stage[pick] == 1:
            continue
        else:
            break
    stage[pick] = -1
    return pick


def contestant_pick_again_random(adjusted_stage):
    """The contestant picks randomly fron the remaining choices."""
    pick = random.randrange(3)
    while adjusted_stage[pick] == -1:
        pick = random.randrange(3)
    return pick;


def contestant_pick_again_same(contestant_pick):
    """Degenerate case, contestant stays with their initial pick."""
    return contestant_pick


def contestant_pick_again_swap(adjusted_stage, pick):
    """Contestant swaps choices with the remaining door."""
    if pick == 0:
        if adjusted_stage[1] == -1:
            return 2
        else:
            return 1
    elif pick == 1:
        if adjusted_stage[0] == -1:
            return 2
        else:
            return 0
    else:
        if adjusted_stage[0] == -1:
            return 1
        else:
            return 0


def run_game():
    """Run a complex game, like the real thing."""
    stage = create_stage()
    contestant_first_pick = random.randrange(3)

    #monty_pick = monty_pick_first_possible(stage, contestant_first_pick)
    monty_pick = monty_pick_random(stage, contestant_first_pick)

    contestant_second_pick = contestant_pick_again_random(stage)
    #contestant_second_pick = contestant_pick_again_same(contestant_first_pick)
    #contestant_second_pick = contestant_pick_again_swap(stage, contestant_first_pick)

    wins = contestant_wins(stage, contestant_second_pick)
    #print (stage, contestant_first_pick, contestant_second_pick, wins)
    return wins


# Simulate many games and count the winners.
while games_run != total_games:
    games_run = games_run + 1 
    if run_game():
        total_wins = total_wins + 1

# And let us know how we did.
print ("Odds of winning:", total_wins * 100.0 / total_games, "%")



