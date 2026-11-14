# Bankroll Management Gambling Test: Does Bet Sizing Change the Outcome?
# Full write-up with charts: https://boosterhand.com/lab/bankroll-management-bet-sizing-simulation/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
# Long-form #14: bankroll management / bet sizing on even-money European roulette (p = 18/37)
import numpy as np, json
rng = np.random.default_rng(1414)
P = 18/37; N = 10000; START = 1000; GOAL = 2000; CAP = 100000; MINBET = 5
def bet_of(name, b):
    if name == 'flat10':  return np.minimum(10, b)
    if name == 'flat50':  return np.minimum(50, b)
    if name == 'flat200': return np.minimum(200, b)
    if name == 'prop2':   return np.minimum(np.maximum(MINBET, np.round(0.02*b)), b)
    if name == 'bold':    return np.minimum(b, GOAL - b)
out = {}
for name in ('flat10', 'flat50', 'flat200', 'prop2', 'bold'):
    b = np.full(N, START, float); alive = np.ones(N, bool); nb = np.zeros(N, int); wag = np.zeros(N); path = []
    for s in range(CAP):
        if not alive.any(): break
        x = bet_of(name, b[alive]); win = rng.random(alive.sum()) < P
        b[alive] += np.where(win, x, -x); wag[alive] += x; nb[alive] += 1
        if len(path) < 6000: path.append(float(b[0]))
        alive &= (b > 0) & (b < GOAL)
    reach = float((b >= GOAL).mean()); loss = START - b.mean()
    out[name] = {'reach': reach, 'broke': float((b <= 0).mean()), 'unfinished': float(alive.mean()),
                 'bets_mean': float(nb.mean()), 'bets_median': float(np.median(nb)),
                 'wagered_mean': float(wag.mean()), 'avg_loss': float(loss),
                 'loss_pct_wagered': float(loss / wag.mean() * 100), 'path0': path[:6000:10]}
    print(name, {k: round(v, 4) for k, v in out[name].items() if k != 'path0'})
out['meta'] = {'p': P, 'players': N, 'start': START, 'goal': GOAL, 'cap': CAP, 'minbet_prop': MINBET, 'edge_pct': (1-2*P)*100}
json.dump(out, open('sim.json', 'w'), indent=1)
# Bold play from $1,000 to $2,000 is a single all-in spin, so 10,000 players is noisy: rerun it with 1,000,000 players.
M = 1_000_000; w = rng.random(M) < P; fin = np.where(w, 2*START, 0.0)
out['bold_1m'] = {'players': M, 'reach': float(w.mean()), 'avg_loss': float(START - fin.mean()), 'wagered_mean': float(START),
                  'loss_pct_wagered': float((START - fin.mean()) / START * 100)}
print('bold_1m', out['bold_1m'])
json.dump(out, open('sim.json', 'w'), indent=1)
