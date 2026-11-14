# I Dropped 1,000,000 Plinko Balls: Plinko Odds, RTP and Risk Levels Simulated

Plinko simulated: 1,000,000 balls per risk level on a 16-row board. The 1,000x slot is 1 in 32,768, 79% of high-risk balls pay 0.2x, and every table keeps ~1%.

## Key results

- On a 16-row board with 50/50 bounces, each edge slot is <strong>1 in 65,536</strong>. Either edge: <strong>1 in 32,768</strong> balls on average.
- <strong>54.5%</strong> of balls land in the middle 3 slots. On high risk, <strong>79%</strong> of balls land in a 0.2x slot.
- All three payout tables return about <strong>99%</strong>. Over 1,000,000 $1 balls the board kept <strong>$9,903</strong> (low), <strong>$8,285</strong> (medium) and <strong>$13,379</strong> (high).
- The 1,000x slot hit <strong>28 times</strong> in a million balls (math expects ~30.5), and the high-risk board still won.
- 10,000 players × 1,000 balls: on high risk <strong>35%</strong> ended ahead, but the median player lost <strong>$49.80</strong> and <strong>1 in 3</strong> lost $100 or more.

Full article with charts and method: [I Dropped 1,000,000 Plinko Balls: Plinko Odds, RTP and Risk Levels Simulated](https://boosterhand.com/lab/plinko-simulation-1-million-balls/)

Video: https://youtu.be/TuKRx07qcSw

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
