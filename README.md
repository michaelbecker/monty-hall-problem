# monty-hall-problem
Test various combinations of the Monty Hall Problem.

## Usage
```
usage: monty.py [-h] [--simple-game] [--monty-pick-random]
                [--monty-pick-first] [--contestant-picks-same]
                [--contestant-picks-swap] [--contestant-picks-random]
                [--number-runs NUMBER_RUNS]

optional arguments:
  -h, --help            show this help message and exit
  --simple-game         Run a simple game, no swapping at all.
  --monty-pick-random   [Default] Monty picks a random goat if possible.
  --monty-pick-first    Monty picks the first goat possible.
  --contestant-picks-same
                        The contestant keeps the first door they picked.
  --contestant-picks-swap
                        [Default] The contestant swaps the door they picked
                        with the other one.
  --contestant-picks-random
                        The contestant "randomly" selects between the two
                        doors left.
  --number-runs NUMBER_RUNS
                        How many times to simulate the game. Default = 10,000
```

