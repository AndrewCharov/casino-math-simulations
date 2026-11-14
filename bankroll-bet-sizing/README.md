# Bankroll Management Gambling Test: Does Bet Sizing Change the Outcome?

Bankroll management tested on 10,000 roulette players per strategy: $10 bets doubled $1,000 just 0.5% of the time, bold play 49%. House kept 2.7% either way.

## Key results

- Trying to turn $1,000 into $2,000 with flat $10 bets worked for just <strong>0.5%</strong> of 10,000 players.
- Bigger bets reached the goal more often: flat $50 <strong>26%</strong>, flat $200 <strong>43%</strong>, one all-in spin <strong>49%</strong>.
- The average $10 player made <strong>3,676 bets</strong> and wagered <strong>$36,758</strong> before the run ended.
- Every strategy lost between <strong>2.6% and 2.8%</strong> of what it bet: the 2.7% house edge, every time.
- Even with bold play, <strong>51%</strong> of players lost the whole $1,000 on a single spin.

Full article with charts and method: [Bankroll Management Gambling Test: Does Bet Sizing Change the Outcome?](https://boosterhand.com/lab/bankroll-management-bet-sizing-simulation/)

Video: https://youtu.be/Jlr4sVuPAVg

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
