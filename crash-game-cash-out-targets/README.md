# Crash Game Strategy: When Should You Cash Out? 60,000 Players Tested

Crash game strategy, simulated: 60,000 players tried 6 cash out targets from 1.1x to 100x. Every target returned 98.7 to 99 cents per $1. Only the risk changed.

## Key results

- In a crash game with a <strong>1% house edge</strong>, the chance to reach any target x is <strong>0.99 ÷ x</strong>, so target × chance is always <strong>0.99</strong>.
- Cashing out at <strong>1.1x</strong> won <strong>90%</strong> of rounds. Waiting for <strong>100x</strong> won under <strong>1%</strong>.
- Every one of 6 targets returned between <strong>98.7 and 99 cents</strong> per $1 bet across <strong>60,000</strong> simulated players.
- After 1,000 rounds, the typical player at 1.1x, 2x or 5x had <strong>$90</strong> left from $100: a loss of 1% of the $1,000 bet.
- Going broke: <strong>0%</strong> at 1.1x, <strong>14%</strong> at 5x, <strong>31%</strong> at 10x and <strong>76%</strong> at 100x.
- At 100x, <strong>41%</strong> doubled their money at some point and the best balance hit <strong>$1,593</strong>. At 1.1x nobody doubled.

Full article with charts and method: [Crash Game Strategy: When Should You Cash Out? 60,000 Players Tested](https://boosterhand.com/lab/crash-game-cash-out-strategy-simulation/)

Video: https://youtu.be/DE4glelNzyg

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
