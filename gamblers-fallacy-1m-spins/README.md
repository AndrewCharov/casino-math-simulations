# Gambler's Fallacy Tested: Is Red Ever Due? 1,000,000 Roulette Spins

The gambler's fallacy, tested on 1,000,000 roulette spins: after 8 blacks in a row, red came up 48.0% of the time. It never got more likely. Here's the data.

## Key results

- In <strong>1,000,000</strong> simulated European roulette spins, red came up <strong>48.6%</strong>, black <strong>48.7%</strong> and green <strong>2.7%</strong>.
- After 1 black, red followed <strong>48.5%</strong> of the time. After 8 blacks in a row: <strong>48.0%</strong>. Red was never due.
- The longest run of one color was <strong>18 in a row</strong>.
- Doubling a $10 bet through that streak would have needed <strong>$2,621,430</strong>.
- "Wait for 5 blacks, then bet red" returned <strong>96.6 cents</strong> per dollar vs <strong>97.2 cents</strong> betting red every spin. Both lose.

Full article with charts and method: [Gambler's Fallacy Tested: Is Red Ever Due? 1,000,000 Roulette Spins](https://boosterhand.com/lab/gamblers-fallacy-1-million-roulette-spins/)

Video: https://youtu.be/882fbI7clX4

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
