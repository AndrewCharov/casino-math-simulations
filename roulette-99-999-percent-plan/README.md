# I Tested a '99.999% Win' Roulette Strategy on 10,000 Players

The two-dozens + triple roulette strategy claims 99.999% wins. 10,000 simulated players: 98.15% hit +$10, yet together they lost $35,667. The exact math.

## Key results

- The plan bets $1 on each of two dozens: 24 of 37 numbers, a <strong>64.9%</strong> win chance per spin. After a loss the stake triples, so any win repays everything plus $1.
- The '99.999%' is the chance of <em>not</em> losing 11 spins in a row. Surviving 11 losses needs <strong>$177,146</strong>. With $1,000 and a $500 table limit, 6 losses in a row end the plan: <strong>99.81%</strong> per win.
- 10,000 players, one session each, stop at +$10: <strong>98.15%</strong> hit the target. The 185 who didn't lost <strong>$719 to $728</strong> each.
- All together they lost <strong>$35,667</strong> of $1,362,006 wagered (<strong>−2.62%</strong>). The math says −2.70%: 1/37 of every dollar.
- Played every day for a year, the plan promised +$3,650. The median player ended at <strong>−$1,476</strong> and <strong>81%</strong> finished the year down.

Full article with charts and method: [I Tested a '99.999% Win' Roulette Strategy on 10,000 Players](https://boosterhand.com/lab/roulette-99-percent-win-strategy-martingale-simulation/)

Video: https://youtu.be/0ZIVluP8CHA

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
