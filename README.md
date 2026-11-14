# Casino Math Simulations

Open-source Python (NumPy) simulations behind the [BoosterHand Lab](https://boosterhand.com/lab/): betting systems, roulette, Plinko, Mines, crash games and slots, each tested on thousands of simulated players with a fixed random seed.

Every folder has a standalone `simulation.py` and a short README with the key results. The full write-ups, with charts and the exact method, are on [boosterhand.com/lab](https://boosterhand.com/lab/).

Models are generic (standard roulette wheels, a 5×5 Mines board, a 1%-edge crash curve, generic slots). They do not reproduce any specific casino's game.

## Simulations

| Folder | Question | Write-up |
| --- | --- | --- |
| [`martingale-10000-players`](./martingale-10000-players) | Martingale Strategy Tested on 10,000 Players: Does It Really Work? | [Read](https://boosterhand.com/lab/martingale-strategy-simulation-10000-players/) |
| [`betting-systems-70000-players`](./betting-systems-70000-players) | Betting Systems Tested on 70,000 Players: Which One Fails Fastest? | [Read](https://boosterhand.com/lab/betting-systems-tested-70000-players/) |
| [`gamblers-fallacy-1m-spins`](./gamblers-fallacy-1m-spins) | Gambler's Fallacy Tested: Is Red Ever Due? 1,000,000 Roulette Spins | [Read](https://boosterhand.com/lab/gamblers-fallacy-1-million-roulette-spins/) |
| [`roulette-european-vs-american`](./roulette-european-vs-american) | European vs American Roulette: Why One Extra Zero Costs You Double | [Read](https://boosterhand.com/lab/roulette-odds-european-vs-american-simulation/) |
| [`crash-game-cash-out-targets`](./crash-game-cash-out-targets) | Crash Game Strategy: When Should You Cash Out? 60,000 Players Tested | [Read](https://boosterhand.com/lab/crash-game-cash-out-strategy-simulation/) |
| [`bankroll-bet-sizing`](./bankroll-bet-sizing) | Bankroll Management Gambling Test: Does Bet Sizing Change the Outcome? | [Read](https://boosterhand.com/lab/bankroll-management-bet-sizing-simulation/) |
| [`plinko-1m-balls`](./plinko-1m-balls) | I Dropped 1,000,000 Plinko Balls: Plinko Odds, RTP and Risk Levels Simulated | [Read](https://boosterhand.com/lab/plinko-simulation-1-million-balls/) |
| [`mines-every-click`](./mines-every-click) | Mines Strategy: The Math Behind Every Click (Odds, Multipliers, RTP) | [Read](https://boosterhand.com/lab/mines-strategy-math-every-click-simulation/) |
| [`roulette-99-999-percent-plan`](./roulette-99-999-percent-plan) | I Tested a '99.999% Win' Roulette Strategy on 10,000 Players | [Read](https://boosterhand.com/lab/roulette-99-percent-win-strategy-martingale-simulation/) |
| [`win-300-a-day-365-days`](./win-300-a-day-365-days) | I Tested the 'Win $300 a Day' Strategy for 365 Days (10,000 Players) | [Read](https://boosterhand.com/lab/win-300-a-day-strategy-simulation-365-days-10000-players/) |
| [`slot-virtual-reel-strip`](./slot-virtual-reel-strip) | How Slot Machines Work: The Hidden Reel Strip (5 Billion Spins Tested) | [Read](https://boosterhand.com/lab/how-slot-machines-work-virtual-reel-strip-hot-cold-myth-simulation/) |
| [`rtp-96-percent-explained`](./rtp-96-percent-explained) | RTP Explained: What 96% RTP Really Means for Your $100 | [Read](https://boosterhand.com/lab/rtp-explained-96-percent-simulation/) |

## Interactive calculators

Exact-math calculators built on the same formulas, free to use and to embed on your own site:

- [Mines calculator](https://boosterhand.com/tools/mines-calculator/): odds and multiplier per click
- [Plinko calculator](https://boosterhand.com/tools/plinko-calculator/): chance of every slot and RTP
- [Martingale calculator](https://boosterhand.com/tools/martingale-calculator/): how many losses a bankroll survives
- [Bankroll calculator](https://boosterhand.com/tools/bankroll-calculator/)
- [Bonus wagering calculator](https://boosterhand.com/tools/wagering-calculator/)
- [Embed code for all widgets](https://boosterhand.com/widgets/)

## Run

```bash
pip install -r requirements.txt
cd martingale-10000-players
python simulation.py
```

Some simulations (365 days × 10,000 players) take a few minutes on a laptop.

## Cite

If you use these numbers, please link to the matching BoosterHand Lab article. See `CITATION.cff`.

## Responsible gambling

The point of every simulation here is the same: no betting system removes the house edge. 18+ only. If gambling stops being fun, take a break.

## Licence

MIT
