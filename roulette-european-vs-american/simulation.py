# European vs American Roulette: Why One Extra Zero Costs You Double
# Full write-up with charts: https://boosterhand.com/lab/roulette-odds-european-vs-american-simulation/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
import numpy as np, json
# Roulette odds: European (37) vs American (38) vs triple-zero (39) wheels.
# 10,000 players per wheel, $100 bankroll, $1 even-money bets (red/black: 18 winning pockets), up to 1,000 spins.
# Extension: same players keep going (cap 50,000 spins) to measure how long the typical $100 lasted.
rng = np.random.default_rng(1111)
M, BANK, SPINS, CAP = 10000, 100, 1000, 50000
CHECK = (100, 300, 500, 1000)
out = {}
for name, N in (('eu', 37), ('us', 38), ('tz', 39)):
    p = 18 / N
    bal = np.full(M, BANK, np.int64); alive = np.ones(M, bool); bust = np.full(M, CAP + 1)
    snap = {}; wagered = 0; curve = []
    for s in range(1, CAP + 1):
        w = rng.random(M) < p
        if s <= SPINS: wagered += int(alive.sum())
        bal[alive] += np.where(w[alive], 1, -1)
        d = alive & (bal <= 0); bust[d] = s; alive &= ~d
        if s <= SPINS and s % 10 == 0: curve.append(float((~alive).mean() * 100))
        if s in CHECK:
            snap[s] = {'broke': float((~alive).mean()), 'ahead': float((bal > BANK).mean()),
                       'median': float(np.median(bal)), 'mean': float(bal.mean())}
            if s == SPINS: lost1000 = float((BANK - bal).sum())
        if s > SPINS and not alive.any(): break
    # single-number $1 bet math (pays 35:1)
    single_ev = (35 * 1 - (N - 1)) / N
    out[name] = {'pockets': N, 'p_even': p, 'edge': 1 - 2 * p, 'single_true_odds': N - 1, 'single_ev': single_ev,
                 'snap': snap, 'loss_per_100_sim': lost1000 / wagered * 100,
                 'median_bust': float(np.median(bust)), 'pct_bust_by_cap': float((bust <= CAP).mean()),
                 'curve': curve}
    print(name, N, 'edge %.4f' % (1 - 2 * p), 'median_bust', out[name]['median_bust'],
          'loss/100 %.2f' % out[name]['loss_per_100_sim'],
          {k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in snap.items()})
json.dump(out, open('sim.json', 'w'), indent=1)
