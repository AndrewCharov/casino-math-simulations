# How Slot Machines Work: The Hidden Reel Strip (5 Billion Spins Tested)

How slot machines work: 22 visible stops, 128 hidden virtual stops. Jackpot odds of 1 in 2,097,152, an exact 95.3% RTP and 5 billion spins testing hot, cold and due machines.

## Key results

- Our reel shows 22 stops, but the RNG picks from <strong>128</strong> hidden virtual stops. The jackpot gets 1 of them, the blanks next to it get 14 each.
- Three jackpots look like <strong>1 in 10,648</strong> (22³). On the hidden reels they are <strong>1 in 2,097,152</strong> (128³): 197 times rarer.
- Every payout × its exact chance adds up to an RTP of <strong>95.3%</strong>. The same paytable on reels where every stop is really 1 in 22 would pay back <strong>255.3%</strong>.
- Over 100,000,000 spins the next spin won <strong>23.0%</strong> of the time overall, <strong>23.0%</strong> after 10+ losses and <strong>22.9%</strong> right after a 100x+ win. No hot or cold machines.
- In 5,000,000,000 spins the jackpot came about <strong>1 in 2.1 million</strong> spins, whether the last one was minutes or 4 million spins ago. Nothing is ever due.

Full article with charts and method: [How Slot Machines Work: The Hidden Reel Strip (5 Billion Spins Tested)](https://boosterhand.com/lab/how-slot-machines-work-virtual-reel-strip-hot-cold-myth-simulation/)

Video: https://youtu.be/Xx6QskcF85I

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
