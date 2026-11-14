# Mines Strategy: The Math Behind Every Click (Odds, Multipliers, RTP)
# Full write-up with charts: https://boosterhand.com/lab/mines-strategy-math-every-click-simulation/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
import numpy as np, json
from math import comb
rng = np.random.default_rng(1616)
T = 25; EDGE = 0.99
P = lambda m, k: comb(T - m, k) / comb(T, k)
out = {'table': {}}
for m in [1, 3, 5, 10, 24]:
    rows = []
    for k in range(1, T - m + 1):
        p = P(m, k); rows.append({'k': k, 'p': p, 'fair': 1 / p, 'pay': EDGE / p})
    out['table'][m] = rows
# step (conditional) survival for 3 mines: click k is safe with prob (22-(k-1))/(25-(k-1))
out['step3'] = [(22 - j) / (25 - j) for j in range(22)]

N = 1_000_000; CH = 100_000
def layouts(n, m):
    r = rng.random((n, T)); idx = np.argpartition(r, m, axis=1)[:, :m]
    b = np.zeros((n, T), bool); np.put_along_axis(b, idx, True, axis=1); return b
CORNERS = [0, 4, 20, 24, 2, 10, 14, 22, 1, 3, 5, 9, 15, 19, 21, 23, 6, 8, 16, 18, 7, 11, 13, 17, 12]
strats = [('3m_1', 3, 1), ('3m_3', 3, 3), ('3m_5', 3, 5), ('3m_10', 3, 10), ('1m_24', 1, 24), ('24m_1', 24, 1)]
out['m1'] = {}
for name, m, k in strats:
    pay = EDGE / P(m, k); wins = 0; first_click_safe = 0
    for _ in range(N // CH):
        b = layouts(CH, m)
        # click order: random tiles each round (a shuffled order per round)
        order = np.argsort(rng.random((CH, T)), axis=1)[:, :k]
        hit = np.take_along_axis(b, order, axis=1)
        wins += int((~hit.any(1)).sum()); first_click_safe += int((~hit[:, 0]).sum())
    ret = wins * pay
    out['m1'][name] = {'mines': m, 'clicks': k, 'p_exact': P(m, k), 'pay': pay, 'wins': wins, 'win_rate': wins / N,
                       'returned': ret, 'net': ret - N, 'net_per_dollar': (ret - N) / N, 'first_click_safe': first_click_safe / N}
# pattern test: 3 mines, 5 clicks, different click patterns, 1,000,000 rounds each
pat = {}
prev = None
for name in ['corners', 'center', 'random', 'avoid_last_mines', 'same_tiles']:
    wins = 0; last = np.zeros(T, bool); last[[0, 1, 2]] = True
    for _ in range(N // CH):
        b = layouts(CH, 3)
        if name == 'corners': hit = b[:, CORNERS[:5]]
        elif name == 'center': hit = b[:, [12, 7, 11, 13, 17]]
        elif name == 'same_tiles': hit = b[:, [3, 8, 16, 19, 21]]
        elif name == 'random': hit = np.take_along_axis(b, np.argsort(rng.random((CH, T)), 1)[:, :5], 1)
        else:
            # pick 5 tiles that were NOT mines in the previous round ("cold" tiles)
            prevb = np.vstack([last[None], b[:-1]])
            sc = rng.random((CH, T)) + prevb * 2.0
            hit = np.take_along_axis(b, np.argsort(sc, 1)[:, :5], 1); last = b[-1]
        wins += int((~hit.any(1)).sum())
    pat[name] = wins / N
out['patterns'] = pat
# corner tile mine frequency vs center (3 mines, 1,000,000 layouts)
b = np.zeros(T, np.int64)
for _ in range(N // CH): b += layouts(CH, 3).sum(0)
out['tile_freq'] = (b / N).tolist()

# players: 10,000 x 500 rounds, $1, $100 budget (stop when down $100)
NP, NR, BUD = 10_000, 500, 100
out['players'] = {}
for name, m, k in [('3m_1', 3, 1), ('3m_5', 3, 5), ('24m_1', 24, 1)]:
    p = P(m, k); pay = EDGE / p
    w = rng.random((NP, NR)) < p
    step = np.where(w, pay - 1, -1.0)
    cum = np.cumsum(step, 1)
    bust = (cum <= -BUD)
    busted = bust.any(1)
    first = np.where(busted, bust.argmax(1), NR - 1)
    final = np.where(busted, cum[np.arange(NP), first], cum[:, -1])
    played = np.where(busted, first + 1, NR)
    hist = np.histogram(np.clip(final, -100, 299.9), bins=np.arange(-100, 301, 10))[0].tolist()
    out['players'][name] = {'p': p, 'pay': pay, 'share_ahead': float((final > 0).mean()), 'median': float(np.median(final)),
        'mean': float(final.mean()), 'worst': float(final.min()), 'best': float(final.max()),
        'share_busted': float(busted.mean()), 'wagered': int(played.sum()), 'net_total': float(final.sum()),
        'net_per_dollar': float(final.sum() / played.sum()), 'p10': float(np.percentile(final, 10)), 'p90': float(np.percentile(final, 90)),
        'max_losing_streak_median': None, 'hist10': hist}
json.dump(out, open('sim.json', 'w'), indent=1)
for m in [1, 3, 5, 10, 24]:
    print(m, [(r['k'], round(r['p'] * 100, 2), round(r['pay'], 2)) for r in out['table'][m][:10]], out['table'][m][-1]['k'], out['table'][m][-1]['pay'])
for n, v in out['m1'].items(): print(n, {a: (round(b, 5) if isinstance(b, float) else b) for a, b in v.items()})
print(pat); print([round(x, 4) for x in out['tile_freq']])
for n, v in out['players'].items(): print(n, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items() if a != 'hist10'})
# convergence: 100,000,000 rounds per strategy (win/lose drawn with the exact survival probability,
# validated above by the 1,000,000 full-layout rounds), running net per $1 at log-spaced checkpoints
NB = 100_000_000; CK = 10_000_000
cps = np.unique(np.round(np.logspace(2, 8, 61)).astype(np.int64))
out['conv_cps'] = cps.tolist(); out['conv'] = {}
for name, m, k in strats:
    p = P(m, k); pay = EDGE / p; vals = []; wins_tot = 0; done = 0
    for c in range(NB // CK):
        w = rng.random(CK) < p; cw = np.cumsum(w)
        sel = cps[(cps > done) & (cps <= done + CK)]
        for s in sel: vals.append(((wins_tot + cw[s - done - 1]) * pay - s) / s)
        wins_tot += int(cw[-1]); done += CK
    out['conv'][name] = vals
    print('conv', name, [round(v * 100, 3) for v in vals[::10]])
json.dump(out, open('sim.json', 'w'), indent=1)
