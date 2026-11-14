# How Slot Machines Work: The Hidden Reel Strip (5 Billion Spins Tested)
# Full write-up with charts: https://boosterhand.com/lab/how-slot-machines-work-virtual-reel-strip-hot-cold-myth-simulation/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
# Long-form #18: "How Slot Machines ACTUALLY Work (The Hidden Reel Strip)"
# Generic 3-reel, 1-line slot. 22 physical stops per reel (11 symbols + 11 blanks),
# mapped to 128 virtual stops. The RNG picks a virtual stop on each reel independently every spin.
import numpy as np, json, itertools, time
rng = np.random.default_rng(1818)
PHYS = ['J', 'b', '7', 'b', '3B', 'b', 'CH', 'b', '1B', 'b', '2B', 'b', '7', 'b', '1B', 'b', 'CH', 'b', '3B', 'b', '2B', 'b']
WTS = {'J': 1, '7': 3, '3B': 4, '2B': 5, '1B': 6, 'CH': 5}
NEAR = 14  # virtual stops given to EACH blank directly above/below the jackpot (stops 21 and 1)
W = [0] * 22
for i, s in enumerate(PHYS):
    if s in WTS: W[i] = WTS[s]
W[1] = W[21] = NEAR
rem = 128 - sum(W); other = [i for i, s in enumerate(PHYS) if s == 'b' and i not in (1, 21)]
for k, i in enumerate(other): W[i] = rem // len(other) + (1 if k < rem % len(other) else 0)
assert sum(W) == 128
V2P = np.repeat(np.arange(22), W)  # virtual stop -> physical stop (virtual stop 0 = jackpot)
PAYT = {'JJJ': 10000, '777': 500, '3B': 200, '2B': 100, '1B': 60, 'anybar': 12, 'ch3': 100, 'ch2': 10, 'ch1': 2, 'none': 0}
BARS = ('1B', '2B', '3B')
def cat(a, b, c):
    s = (a, b, c)
    if s == ('J',) * 3: return 'JJJ'
    if s == ('7',) * 3: return '777'
    if a == b == c and a in BARS: return a
    if all(x in BARS for x in s): return 'anybar'
    n = sum(x == 'CH' for x in s)
    return 'ch%d' % n if n else 'none'
out = {'phys': PHYS, 'weights': W, 'paytable': PAYT}
# ---------- exact math ----------
pv = np.array(W) / 128; pp = np.ones(22) / 22
def exact(p):
    rtp = 0; hit = 0; by = {}
    for i, j, k in itertools.product(range(22), repeat=3):
        c = cat(PHYS[i], PHYS[j], PHYS[k]); pr = p[i] * p[j] * p[k]; v = PAYT[c]
        rtp += v * pr; hit += pr * (v > 0); e = by.setdefault(c, [0, 0]); e[0] += pr; e[1] += v * pr
    return rtp, hit, by
r, h, by = exact(pv); rp, hp, byp = exact(pp)
out['exact'] = {'rtp': r, 'hit': h, 'by': by, 'rtp_if_physical': rp, 'hit_if_physical': hp, 'by_physical': byp,
                'p_jackpot_virtual': (1 / 128) ** 3, 'p_jackpot_physical': (1 / 22) ** 3,
                'one_in_virtual': 128 ** 3, 'one_in_physical': 22 ** 3,
                'stop_share_virtual': [w / 128 for w in W],
                'near_miss_virtual': (1 / 128) ** 2 * (2 * NEAR / 128), 'near_miss_physical': (1 / 22) ** 2 * (2 / 22)}
print('exact RTP', r, 'hit', h, 'phys RTP', rp, 'phys hit', hp)
print({k: (round(v[0], 6), round(v[1], 5)) for k, v in by.items()})
# payout lookup over virtual stops
cv = [cat(PHYS[V2P[a]], PHYS[V2P[b]], PHYS[V2P[c]]) for a, b, c in itertools.product(range(128), repeat=3)]
PAYV = np.array([PAYT[c] for c in cv], np.float32)
CATS = list(PAYT.keys()); CATI = np.array([CATS.index(c) for c in cv], np.int8)
def spin(n):
    a = rng.integers(0, 128, n, dtype=np.int32); b = rng.integers(0, 128, n, dtype=np.int32); c = rng.integers(0, 128, n, dtype=np.int32)
    return a, (a << 14) | (b << 7) | c
# ---------- 1,000,000 spins ----------
N1 = 1_000_000
a, idx = spin(N1); pay = PAYV[idx]
cps = np.unique(np.round(np.logspace(1, 6, 51)).astype(np.int64)); cs = np.cumsum(pay)
out['m1'] = {'spins': N1, 'returned': float(pay.sum()), 'rtp': float(pay.sum() / N1), 'hit': float((pay > 0).mean()),
             'counts': {c: int((CATI[idx] == i).sum()) for i, c in enumerate(CATS)}, 'jackpots': int((idx == 0).sum()),
             'cps': cps.tolist(), 'rtp_curve': (cs[cps - 1] / cps).tolist(),
             'reel1_phys_freq': (np.bincount(V2P[a], minlength=22) / N1).tolist(),
             'biggest': float(pay.max())}
print('1M', {k: v for k, v in out['m1'].items() if k not in ('cps', 'rtp_curve', 'reel1_phys_freq')})
# ---------- 100,000,000 spins: RTP + hot/cold tests ----------
NB = 100_000_000; CK = 10_000_000; t0 = time.time()
cps2 = np.unique(np.round(np.logspace(4, 8, 41)).astype(np.int64)); curve = []
TH = [0, 5, 10, 20, 30]          # losing streak of at least N spins before this spin
st_n = {k: 0 for k in TH}; st_w = {k: 0 for k in TH}; st_p = {k: 0.0 for k in TH}
BIG = 100                           # "right after a big win" = previous spin paid 100x or more
aw_n = 0; aw_w = 0; aw_p = 0.0; ret = 0.0; wins = 0; last_win = -1; prev_pay = 0.0; done = 0; maxdry = 0
for ch in range(NB // CK):
    _, idx = spin(CK); pay = PAYV[idx].astype(np.float64); win = pay > 0
    gi = np.arange(done, done + CK)
    lw = np.maximum.accumulate(np.where(win, gi, -1)); lw = np.maximum(lw, last_win)
    prev_lw = np.r_[last_win, lw[:-1]]                # last win strictly before each spin
    streak = gi - 1 - prev_lw                            # losing spins in a row right before this spin
    maxdry = max(maxdry, int(streak.max()))
    for k in TH:
        m = streak >= k; st_n[k] += int(m.sum()); st_w[k] += int(win[m].sum()); st_p[k] += float(pay[m].sum())
    pp_ = np.r_[prev_pay, pay[:-1]]; m = pp_ >= BIG
    aw_n += int(m.sum()); aw_w += int(win[m].sum()); aw_p += float(pay[m].sum())
    cs = np.cumsum(pay) + ret
    sel = cps2[(cps2 > done) & (cps2 <= done + CK)]
    curve += (cs[sel - done - 1] / sel).tolist()
    ret = float(cs[-1]); wins += int(win.sum()); last_win = int(lw[-1]); prev_pay = float(pay[-1]); done += CK
out['m100'] = {'spins': NB, 'rtp': ret / NB, 'hit': wins / NB, 'cps': cps2.tolist(), 'rtp_curve': curve, 'max_dry': maxdry,
               'after_streak': {str(k): {'n': st_n[k], 'hit': st_w[k] / st_n[k], 'rtp': st_p[k] / st_n[k]} for k in TH},
               'after_big': {'n': aw_n, 'hit': aw_w / aw_n, 'rtp': aw_p / aw_n}}
print('100M', round(time.time() - t0), 's', {k: v for k, v in out['m100'].items() if k not in ('cps', 'rtp_curve')})
json.dump(out, open('sim.json', 'w'), indent=1)
# ---------- 1,000,000,000 spins: jackpots only, "due" test ----------
NJ = 5_000_000_000; CJ = 50_000_000; t0 = time.time(); jp = []
for ch in range(NJ // CJ):
    a = rng.integers(0, 128, CJ, dtype=np.uint8); m = a == 0
    b = rng.integers(0, 128, CJ, dtype=np.uint8); m &= b == 0
    c = rng.integers(0, 128, CJ, dtype=np.uint8); m &= c == 0
    jp += (np.nonzero(m)[0] + ch * CJ).tolist()
jp = np.array(jp, np.int64); gaps = np.diff(jp)
# exposure by "spins since last jackpot" buckets (after the first jackpot)
B = [0, 500_000, 1_000_000, 2_000_000, 4_000_000, 10 ** 12]
exp_ = np.zeros(len(B) - 1); hits = np.zeros(len(B) - 1)
ends = np.r_[jp[1:], NJ]; starts = jp
for s, e in zip(starts, ends):
    L = e - s  # spins after jackpot at s: s+1 .. e (the spin at e is a jackpot if e < NJ); since = 1..L
    for bi in range(len(B) - 1):
        lo, hi = B[bi] + 1, B[bi + 1]
        exp_[bi] += max(0, min(L, hi) - lo + 1)
        if e < NJ and lo <= L <= hi: hits[bi] += 1
out['mjp'] = {'spins': NJ, 'jackpots': int(len(jp)), 'expected': NJ / 128 ** 3, 'gap_median': float(np.median(gaps)), 'gap_mean': float(gaps.mean()),
                'gap_max': int(gaps.max()), 'gap_min': int(gaps.min()), 'share_gaps_over_4m': float((gaps > 4_000_000).mean()),
                'buckets': [{'lo': B[i], 'hi': B[i + 1], 'exposure': float(exp_[i]), 'jackpots': int(hits[i]),
                             'one_in': float(exp_[i] / hits[i]) if hits[i] else None} for i in range(len(B) - 1)],
                'gaps_hist': np.histogram(np.clip(gaps, 0, 9_999_999), bins=np.arange(0, 10_000_001, 500_000))[0].tolist(),
                'next1m_after_jp': int((gaps <= 1_000_000).sum())}
print('1B', round(time.time() - t0), 's', {k: v for k, v in out['mjp'].items() if k != 'gaps_hist'})
json.dump(out, open('sim.json', 'w'), indent=1)
# ---------- 10,000 players x 1,000 spins of $1 ----------
NP, NS = 10_000, 1000; fin = np.zeros(NP); big = np.zeros(NP); jph = 0; best_spin = 0.0
for p0 in range(0, NP, 1000):
    _, idx = spin(1000 * NS); pay = PAYV[idx].reshape(1000, NS).astype(np.float64)
    fin[p0:p0 + 1000] = pay.sum(1) - NS; big[p0:p0 + 1000] = pay.max(1); jph += int((idx == 0).sum())
hist = np.histogram(np.clip(fin, -1000, 1990), bins=np.arange(-1000, 2001, 50))[0].tolist()
out['players'] = {'n': NP, 'spins': NS, 'ahead': float((fin > 0).mean()), 'median': float(np.median(fin)), 'mean': float(fin.mean()),
                  'best': float(fin.max()), 'worst': float(fin.min()), 'p10': float(np.percentile(fin, 10)), 'p90': float(np.percentile(fin, 90)),
                  'jackpot_players': jph, 'hist50': hist, 'total_rtp': float((fin.sum() + NP * NS) / (NP * NS)),
                  'lost_over_100': float((fin < -100).mean())}
print('players', {k: v for k, v in out['players'].items() if k != 'hist50'})
json.dump(out, open('sim.json', 'w'), indent=1)
