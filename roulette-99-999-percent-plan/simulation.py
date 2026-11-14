# I Tested a '99.999% Win' Roulette Strategy on 10,000 Players
# Full write-up with charts: https://boosterhand.com/lab/roulette-99-percent-win-strategy-martingale-simulation/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
# Long-form #17: the "99.999% win" roulette plan (two dozens + triple after a loss), single-zero wheel.
# Plan: $1,000 bankroll, $1 on each of two dozens (1st + 2nd, numbers 1-24) = $2 per spin.
# Win (1-24, 24/37): one dozen pays 2:1, the other loses -> net +half the stake. Loss (0 or 25-36, 13/37): lose the stake.
# After a loss, triple the stake (2, 6, 18, 54, 162, 486 ...) so the next win recovers everything + $1.
# Session ends at +$10 profit (target), or when the next stake is unaffordable (bankroll) or over the table limit ($500 per bet).
import numpy as np, json
from fractions import Fraction
rng = np.random.default_rng(1717)
P_WIN = Fraction(24, 37); Q = 1 - P_WIN
BANK, BASE, LIMIT, TARGET = 1000, 2, 500, 10
out = {'p_win': float(P_WIN), 'q': float(Q), 'edge_per_dollar': float((P_WIN * 1 - Q * 2) / 2)}
out['ladder'] = [BASE * 3 ** k for k in range(12)]
out['ladder_cum'] = [sum(out['ladder'][:k + 1]) for k in range(12)]
out['streak_p'] = {k: float(Q ** k) for k in range(1, 13)}

def max_losses(bank, base, limit, target):
    # number of consecutive losses that kills the chain (cannot place the next tripled bet), worst case gains=0
    lost = 0; k = 0
    while True:
        st = base * 3 ** k
        if st > bank - lost or st / 2 > limit: return k
        lost += st; k += 1

def exact(bank, base, limit, target):
    """exact session success + expected result via cycle DP (bankroll only grows by +base/2 per cycle, K const check)"""
    unit = Fraction(base, 2); T = int(Fraction(target) / unit)
    succ = Fraction(1); ev = Fraction(0); turn = Fraction(0)
    # per cycle: K = max losses survivable given current gains g; P(fail) = Q^K
    for c in range(T):
        g = c * unit; K = max_losses(bank + g, base, limit, target)
        pf = Q ** K
        # expected wager within a cycle: stake k placed if first k results are losses (k < K)
        ew = sum(Q ** k * base * 3 ** k for k in range(K))
        loss_bust = base * (3 ** K - 1) // 2
        ev += succ * (pf * (-loss_bust))  # bust in this cycle: lose that, gains g are already counted below
        turn += succ * ew
        succ *= (1 - pf)
    # expected result = sum over cycles completed of +unit (counted while alive) + bust losses
    # recompute cleanly: E = sum_c P(alive at start of c) * [(1-pf_c)*unit - pf_c*loss_c]
    alive = Fraction(1); E = Fraction(0)
    for c in range(T):
        g = c * unit; K = max_losses(bank + g, base, limit, target); pf = Q ** K
        E += alive * ((1 - pf) * unit - pf * (base * (3 ** K - 1) // 2)); alive *= (1 - pf)
    return {'K': max_losses(bank, base, limit, target), 'p_cycle_fail': float(Q ** max_losses(bank, base, limit, target)),
            'success': float(succ), 'ev': float(E), 'turnover': float(turn), 'ev_per_dollar': float(E / turn), 'cycles': T}

out['exact_main'] = exact(BANK, BASE, LIMIT, TARGET)
versions = [('main +$10', 1000, 2, 500, 10), ('+$1', 1000, 2, 500, 1), ('+$100', 1000, 2, 500, 100),
            ('$10 bets, +$100', 1000, 20, 500, 100),
            ('7 steps: $2,186, no limit', 2186, 2, 10 ** 9, 10), ('11 steps: $177,146, no limit', 177146, 2, 10 ** 9, 10),
            ('$177,146 with $500 limit', 177146, 2, 500, 10)]
out['versions'] = [{'name': n, 'bank': b, 'base': s, 'limit': l, 'target': tg, **exact(b, s, l, tg)} for n, b, s, l, tg in versions]

# ---------------- Monte Carlo: 10,000 players, one session each, spin by spin ----------------
def sessions(n, bank, base, limit, target, rng, keep_first=0):
    B = np.full(n, float(bank)); step = np.zeros(n, np.int64); alive = np.ones(n, bool); bust = np.zeros(n, bool)
    spins = np.zeros(n, np.int64); wag = np.zeros(n); wins = np.zeros(n, np.int64); streak = np.zeros(n, np.int64); maxst = np.zeros(n, np.int64)
    first = []
    while alive.any():
        st = base * 3.0 ** step
        cant = alive & ((st > B) | (st / 2 > limit))
        bust |= cant; alive &= ~cant
        idx = np.flatnonzero(alive)
        if not len(idx): break
        num = rng.integers(0, 37, len(idx)); w = (num >= 1) & (num <= 24)
        if keep_first and len(first) < keep_first: first.append(int(num[0]) if alive[0] else -1)
        s = st[idx]; spins[idx] += 1; wag[idx] += s
        B[idx] += np.where(w, s / 2, -s); wins[idx] += w
        step[idx] = np.where(w, 0, step[idx] + 1)
        streak[idx] = np.where(w, 0, streak[idx] + 1); maxst[idx] = np.maximum(maxst[idx], streak[idx])
        done = alive & (B - bank >= target - 1e-9); alive &= ~done
    return {'res': B - bank, 'bust': bust, 'spins': spins, 'wag': wag, 'wins': wins, 'maxst': maxst}

NP = 10_000
r = sessions(NP, BANK, BASE, LIMIT, TARGET, rng)
res = r['res']
out['players'] = {'n': NP, 'hit_target': float((~r['bust']).mean()), 'busted': float(r['bust'].mean()), 'n_busted': int(r['bust'].sum()),
    'mean': float(res.mean()), 'median': float(np.median(res)), 'total': float(res.sum()), 'turnover': float(r['wag'].sum()),
    'total_per_dollar': float(res.sum() / r['wag'].sum()), 'expected_total': float(-res.size * 0 + out['edge_per_dollar'] * r['wag'].sum()),
    'spins_total': int(r['spins'].sum()), 'spins_won': int(r['wins'].sum()), 'spin_win_rate': float(r['wins'].sum() / r['spins'].sum()),
    'bust_mean': float(res[r['bust']].mean()), 'bust_min': float(res[r['bust']].min()), 'bust_max': float(res[r['bust']].max()),
    'win_value': float(res[~r['bust']].mean()), 'wins_total': float(res[~r['bust']].sum()), 'bust_total': float(res[r['bust']].sum()),
    'avg_spins': float(r['spins'].mean()), 'max_streak': int(r['maxst'].max()), 'avg_wager_session': float(r['wag'].mean()),
    'bust_flags_first': r['bust'][:10000].astype(int).tolist()}
# player 100x100 grid order: bust flags already in out (for the dot grid)

# ---------------- +$100 target, same plan (10,000 players) ----------------
r2 = sessions(NP, BANK, BASE, LIMIT, 100, rng)
out['players100'] = {'hit_target': float((~r2['bust']).mean()), 'busted': float(r2['bust'].mean()), 'mean': float(r2['res'].mean()),
    'median': float(np.median(r2['res'])), 'total_per_dollar': float(r2['res'].sum() / r2['wag'].sum()), 'bust_mean': float(r2['res'][r2['bust']].mean())}

# ---------------- a year: 365 daily sessions (fresh $1,000 plan each day, topped up after a bust) ----------------
DAYS = 365
yr = np.zeros(NP); ywag = np.zeros(NP); ybust = np.zeros(NP, np.int64); never = np.ones(NP, bool)
path_sel = [0, 1, 2, 3, 4]; paths = np.zeros((DAYS + 1, NP))
for d in range(DAYS):
    rr = sessions(NP, BANK, BASE, LIMIT, TARGET, rng)
    yr += rr['res']; ywag += rr['wag']; ybust += rr['bust']; paths[d + 1] = yr
yhist = np.histogram(np.clip(yr, -10000, 3649.9), bins=np.arange(-10000, 3651, 250))[0].tolist()
out['year'] = {'days': DAYS, 'promised': DAYS * TARGET, 'mean': float(yr.mean()), 'median': float(np.median(yr)), 'share_ahead': float((yr > 0).mean()),
    'share_no_bust': float((ybust == 0).mean()), 'mean_busts': float(ybust.mean()), 'best': float(yr.max()), 'worst': float(yr.min()),
    'p10': float(np.percentile(yr, 10)), 'p90': float(np.percentile(yr, 90)), 'per_dollar': float(yr.sum() / ywag.sum()),
    'turnover_mean': float(ywag.mean()), 'hist250': yhist, 'bust_counts': np.bincount(ybust, minlength=16)[:16].tolist(),
    'paths': {str(i): [round(float(paths[d, i]), 2) for d in range(0, DAYS + 1, 5)] for i in range(40)},
    'mean_path': [round(float(paths[d].mean()), 2) for d in range(0, DAYS + 1, 5)]}
json.dump(out, open('sim.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('players', 'year', 'versions', 'ladder', 'ladder_cum', 'streak_p')}, indent=0))
print('ladder', out['ladder'][:12], out['ladder_cum'][:12])
print('streak', {k: round(v * 100, 5) for k, v in out['streak_p'].items()})
for v in out['versions']: print(v['name'], v['K'], round(v['p_cycle_fail'] * 100, 4), 'succ', round(v['success'] * 100, 3), 'ev', round(v['ev'], 3), 'ev/$', round(v['ev_per_dollar'] * 100, 3))
print({k: v for k, v in out['players'].items() if k != 'bust_flags_first'})
print(out['players100'])
print({k: v for k, v in out['year'].items() if k not in ('paths', 'mean_path', 'hist250')}); print(out['year']['hist250'])
