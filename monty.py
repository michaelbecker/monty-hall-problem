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
import argparse

# The stage is what we work from. 
#  0 => goat
#  1 => car
# -1 => Monty opened the door and showed us the goat.
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
    elif stage[1] == 0 and contestant_pick != 1:
        stage[1] = -1
    else:
        stage[2] = -1


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


def contestant_pick_again_random(adjusted_stage, contestant_first_pick):
    """The contestant picks randomly fron the remaining choices."""
    pick = random.randrange(3)
    while adjusted_stage[pick] == -1:
        pick = random.randrange(3)
    return pick;


def contestant_pick_again_same(adjusted_stage, contestant_first_pick):
    """Degenerate case, contestant stays with their initial pick."""
    return contestant_first_pick


def contestant_pick_again_swap(adjusted_stage, contestant_first_pick):
    """Contestant swaps choices with the remaining door."""
    if contestant_first_pick == 0:
        if adjusted_stage[1] == -1:
            return 2
        else:
            return 1
    elif contestant_first_pick == 1:
        if adjusted_stage[0] == -1:
            return 2
        else:
            return 0
    else:
        if adjusted_stage[0] == -1:
            return 1
        else:
            return 0


def run_normal_game():
    """Run a complex game, like the real thing."""
    stage = create_stage()
    contestant_first_pick = random.randrange(3)

    montys_pick_algorithm(stage, contestant_first_pick)

    contestant_second_pick = contestants_second_pick_algorithm(stage, contestant_first_pick)

    wins = contestant_wins(stage, contestant_second_pick)
    #print (stage, contestant_first_pick, contestant_second_pick, wins)
    return wins


# Lets take some arguments so we can experiment without changing code.
parser = argparse.ArgumentParser()
parser.add_argument("--simple-game", action='store_true', 
        help="Run a simple game, no swapping at all.")
parser.add_argument("--monty-pick-random", action='store_true', 
        help="[Default] Monty picks a random goat if possible.")
parser.add_argument("--monty-pick-first", action='store_true', 
        help="Monty picks the first goat possible.")
parser.add_argument("--contestant-picks-same", action='store_true', 
        help="The contestant keeps the first door they picked.")
parser.add_argument("--contestant-picks-swap", action='store_true', 
        help="[Default] The contestant swaps the door they picked with the other one.")
parser.add_argument("--contestant-picks-random", action='store_true', 
        help="The contestant \"randomly\" selects between the two doors left.")
parser.add_argument("--number-runs", type=int, 
        help="How many times to simulate the game. Default = 10,000")
args = parser.parse_args()


# Do this at the start, we are going to use this module a lot.
random.seed();

total_games = 10000
games_run = 0
total_wins = 0

# How many test runs?
if args.number_runs:
    total_games = args.number_runs

if args.simple_game:
    # If its a "simple" game, we don't use any other algorithms.
    run_game = run_simple_game
else:
    run_game = run_normal_game

    # How will Monty pick a goat to show us?
    if args.monty_pick_random:
        montys_pick_algorithm = monty_pick_random
    elif args.monty_pick_first:
        montys_pick_algorithm = monty_pick_first_possible
    else:
        montys_pick_algorithm = monty_pick_random

    # How will the contestant pick when presented with a second choice?
    if args.contestant_picks_same:
        contestants_second_pick_algorithm = contestant_pick_again_same
    elif args.contestant_picks_swap:
        contestants_second_pick_algorithm = contestant_pick_again_swap
    elif args.contestant_picks_random:
        contestants_second_pick_algorithm = contestant_pick_again_random
    else:
        contestants_second_pick_algorithm = contestant_pick_again_swap


# Simulate many games and count the winners.
while games_run != total_games:
    games_run = games_run + 1 
    if run_game():
        total_wins = total_wins + 1


# And let us know how we did.
print ("Game Type:", run_game.__name__)
print ("Monty's Selection Algorithm:", contestants_second_pick_algorithm.__name__)
print ("Contestant's Second Pick Algorithm:", montys_pick_algorithm.__name__)
print ("Total Games:", total_games)
print ("Games Won:", total_wins)
print ("Odds of winning:", total_wins * 100.0 / total_games, "%")



