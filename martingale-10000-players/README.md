# Martingale Strategy Tested on 10,000 Players: Does It Really Work?

Martingale strategy simulated on 10,000 roulette players: the median player was up $390 after 100 spins, but 79% were broke after 1,000. Here's why.

## Key results

- A $1,000 bankroll with a $10 base bet survives <strong>6 losses in a row</strong>, not 7.
- 7 losses in a row is about <strong>1 in 106</strong> per spin, yet it showed up in <strong>99%</strong> of 1,000-spin sessions.
- After 100 spins, 62% of players were ahead and the median player was <strong>up $390</strong>.
- After 1,000 spins, <strong>79% were broke</strong> and only <strong>18.8%</strong> were ahead.
- The average player bet <strong>$14,726</strong> and lost <strong>$379</strong>: 2.6% of all bets, close to the 2.7% house edge.
- Stopping at +$100 worked for 89%, but the average player still lost <strong>$23</strong>.

Full article with charts and method: [Martingale Strategy Tested on 10,000 Players: Does It Really Work?](https://boosterhand.com/lab/martingale-strategy-simulation-10000-players/)

Video: https://youtu.be/vHSX0NPCVq4

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
