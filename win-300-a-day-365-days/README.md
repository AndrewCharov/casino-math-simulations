# I Tested the 'Win $300 a Day' Strategy for 365 Days (10,000 Players)

Stop when you're up $300 every day and make $109,500 a year? 10,000 simulated players, 365 days: 63% winning days, median −$64,700, nobody finished up.

## Key results

- The plan: a fresh $1,000 every day, $50 on red (European roulette), stop at +$300 or when the $1,000 is gone. Exact math: <strong>63.3%</strong> of days end at +$300.
- A green day adds $300, a red day costs $1,000. Break-even needs <strong>77%</strong> green days (281 of 365). The luckiest of 10,000 players got 264.
- After a year the promised +$109,500 became a median of <strong>−$64,700</strong>. Best player: <strong>−$21,800</strong>. Players up: <strong>0 of 10,000</strong>.
- Each player bet <strong>$2.39 million</strong> in a year. All together: $23.9 billion wagered, $648.5M lost, against an expected <strong>$647.1M</strong> (1/37 of it).
- Bigger $100 bets: 70.4% green days, median −$30,900, 38 players up. A game with a 0.5% edge: 74.6% green days, median −$11,400, <strong>16%</strong> up.

Full article with charts and method: [I Tested the 'Win $300 a Day' Strategy for 365 Days (10,000 Players)](https://boosterhand.com/lab/win-300-a-day-strategy-simulation-365-days-10000-players/)

Video: https://youtu.be/bwmpKeFq2c0

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
