# Mines Strategy: The Math Behind Every Click (Odds, Multipliers, RTP)

Mines odds and multipliers on a 5×5 board, calculated for every click. 3 mines: 88% safe first click, 19.8% after 10. Every strategy ends at about −1%.

## Key results

- With 3 mines the first click is <strong>88%</strong> safe. Survival compounds down fast: <strong>49.6%</strong> after 5 clicks, <strong>19.8%</strong> after 10.
- A fair multiplier is 1 ÷ survival chance. A 99% RTP game pays <strong>0.99 ÷ chance</strong>: 2.00x at 5 clicks, 5.00x at 10 (3 mines).
- 1,000,000 rounds per strategy: every one lost money. Over <strong>100,000,000</strong> rounds each, all landed between <strong>−0.99% and −1.12%</strong> per $1.
- Corners, center or avoiding last round's mines: all survived <strong>49.5–49.6%</strong> of the time. Every tile was a mine about <strong>12%</strong> of the time. No hot tiles.
- 10,000 players × 500 rounds: 24 mines/1 click had the best winner (<strong>+$415.75</strong>), but the median player lost <strong>$29.75</strong> and <strong>37%</strong> lost their whole $100.

Full article with charts and method: [Mines Strategy: The Math Behind Every Click (Odds, Multipliers, RTP)](https://boosterhand.com/lab/mines-strategy-math-every-click-simulation/)

Video: https://youtu.be/HW9mNmXp8is

## Run it

```bash
pip install numpy
python simulation.py
```

Fixed random seed, so you get the same numbers as the article. Change the parameters at the top of the script to test your own variant.
