# I Tested the 'Win $300 a Day' Strategy for 365 Days (10,000 Players)
# Full write-up with charts: https://boosterhand.com/lab/win-300-a-day-strategy-simulation-365-days-10000-players/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
# Long-form #19: the "win $300 a day" plan, 10,000 players x 365 days.
# Daily plan: fresh $1,000 bankroll, flat even-money bets, stop at +$300 or when the day's $1,000 is gone.
# Main: European roulette, $50 on red (win 18/37, edge 1/37). Variants: $100 bets (roulette), and $50 bets on
# "a game with a 0.5% edge" modeled as an even-money bet with win chance 0.4975 (not exact blackjack rules).
# Every spin is simulated (Monte Carlo, NumPy, fixed seed). Exact gambler's-ruin math as a cross-check.
import numpy as np, json, base64
rng = np.random.default_rng(1919)
NP, DAYS, BANK, TARGET = 10_000, 365, 1000, 300
VARS = [('main', 'Roulette, $50 on red', 50, 18 / 37), ('big', 'Roulette, $100 on red', 100, 18 / 37),
        ('low', 'A 0.5% edge game, $50 bets', 50, 0.4975)]

def exact(bet, p, bank=BANK, target=TARGET):
    """gambler's ruin: start i units, stop at 0 or N units. P(reach N), expected spins."""
    i, N = bank // bet, (bank + target) // bet; q = 1 - p; r = q / p
    pw = (1 - r ** i) / (1 - r ** N) if p != q else i / N
    dur = i / (q - p) - N / (q - p) * (1 - r ** i) / (1 - r ** N) if p != q else i * (N - i)
    ev = pw * target - (1 - pw) * bank
    return {'p_win_day': pw, 'spins': dur, 'wager': dur * bet, 'ev_day': ev, 'edge': q - p}

def days(n, bet, p, rng, track=()):
    """simulate n independent days, spin by spin. returns result (+300/-1000), spins. track: indices to record walks"""
    i0, N = BANK // bet, (BANK + TARGET) // bet
    pos = np.full(n, i0, np.int16); spins = np.zeros(n, np.int32); act = np.arange(n)
    walks = {k: [i0] for k in track}
    while len(act):
        w = rng.random(len(act)) < p
        pos[act] += np.where(w, 1, -1).astype(np.int16); spins[act] += 1
        for k in track:
            if len(walks[k]) <= spins[k]: walks[k].append(int(pos[k]))  # one entry per spin taken
        act = act[(pos[act] > 0) & (pos[act] < N)]
    win = pos == N
    return win, spins, {k: [v * bet - BANK for v in walks[k]] for k in walks}

out = {'n': NP, 'days': DAYS, 'bank': BANK, 'target': TARGET, 'promised': DAYS * TARGET,
       'breakeven_winrate': BANK / (BANK + TARGET), 'exact': {}, 'vars': {}}
for b in [10, 20, 25, 50, 100]:
    out['exact'][f'roulette_{b}'] = exact(b, 18 / 37)
out['exact']['low_50'] = exact(50, 0.4975); out['exact']['low_100'] = exact(100, 0.4975)
out['exact']['fair_50'] = exact(50, 0.5)

CK = [1, 7, 30, 90, 180, 365]
for key, name, bet, p in VARS:
    # day index = player * 365 + day
    track = tuple(range(0, 40)) if key == 'main' else ()
    win, spins, walks = days(NP * DAYS, bet, p, rng, track)
    W = win.reshape(NP, DAYS); SP = spins.reshape(NP, DAYS)
    res = np.where(W, TARGET, -BANK); cum = res.cumsum(1); yr = cum[:, -1]
    wag = SP.sum(1) * bet; wins = W.sum(1)
    # longest winning streak per player
    best_streak = np.zeros(NP, np.int32); cur = np.zeros(NP, np.int32); st_end = np.zeros(NP, np.int32)
    for d in range(DAYS):
        cur = np.where(W[:, d], cur + 1, 0); upd = cur > best_streak; best_streak[upd] = cur[upd]; st_end[upd] = d
    first_loss = np.where((~W).any(1), (~W).argmax(1) + 1, 0)
    edge = 1 - 2 * p
    v = {'name': name, 'bet': bet, 'p': p, 'edge': edge,
         'win_day_share': float(W.mean()), 'mean_day': float(res.mean()), 'spins_per_day': float(SP.mean()),
         'wager_per_day': float(SP.mean() * bet), 'max_spins_day': int(SP.max()),
         'mean': float(yr.mean()), 'median': float(np.median(yr)), 'p10': float(np.percentile(yr, 10)), 'p90': float(np.percentile(yr, 90)),
         'best': int(yr.max()), 'worst': int(yr.min()), 'share_up': float((yr > 0).mean()), 'n_up': int((yr > 0).sum()),
         'wins_mean': float(wins.mean()), 'wins_min': int(wins.min()), 'wins_max': int(wins.max()), 'wins_needed': int(np.ceil(DAYS * BANK / (BANK + TARGET) + 1e-9)),
         'wagered_total': float(wag.sum()), 'lost_total': float(-yr.sum()), 'expected_loss': float(edge * wag.sum()),
         'loss_per_dollar': float(-yr.sum() / wag.sum()), 'wagered_mean': float(wag.mean()),
         'win_total': float((res > 0).sum() * TARGET), 'loss_total_days': float((res < 0).sum() * BANK),
         'n_win_days': int(W.sum()), 'n_loss_days': int((~W).sum()),
         'share_up_at': {d: float((cum[:, d - 1] > 0).mean()) for d in CK},
         'max_streak': int(best_streak.max()), 'mean_max_streak': float(best_streak.mean()),
         'first_loss_mean': float(first_loss[first_loss > 0].mean()), 'no_loss_week': float(W[:, :7].all(1).mean())}
    hw = np.bincount(wins, minlength=DAYS + 1)
    v['wins_hist'] = hw.tolist()
    if key == 'main':
        sp = int(best_streak.argmax())
        v['streak_player'] = {'id': sp, 'len': int(best_streak[sp]), 'end_day': int(st_end[sp]) + 1, 'start_day': int(st_end[sp] - best_streak[sp] + 2),
                              'peak': int(cum[sp].max()), 'peak_day': int(cum[sp].argmax()) + 1, 'final': int(yr[sp]), 'wins': int(wins[sp])}
        bp = int(yr.argmax()); v['best_player'] = {'id': bp, 'final': int(yr[bp]), 'wins': int(wins[bp])}
        # all players' day outcomes, packed bits (row = player), for the live animations
        bits = np.packbits(W.astype(np.uint8), axis=1)  # 10000 x 46 bytes
        v['bits_b64'] = base64.b64encode(bits.tobytes()).decode()
        v['p1'] = {'days': W[0].astype(int).tolist(), 'final': int(yr[0]), 'wins': int(wins[0]), 'spins': SP[0].tolist()[:40]}
        v['walks'] = {str(k): walks[k] for k in track}
        v['in_red_by_day'] = [int((cum[:, d] < 0).sum()) for d in range(DAYS)]
        v['up_by_day'] = [int((cum[:, d] > 0).sum()) for d in range(DAYS)]
        v['day_spins_hist'] = np.bincount(np.minimum(SP.ravel(), 999) // 20, minlength=50).tolist()
        v['loss_days_mean_spins'] = float(SP[~W].mean()); v['win_days_mean_spins'] = float(SP[W].mean())
    out['vars'][key] = v
    print(key, {k: (round(x, 4) if isinstance(x, float) else x) for k, x in v.items() if k not in ('wins_hist', 'bits_b64', 'p1', 'walks', 'in_red_by_day', 'up_by_day', 'day_spins_hist')})
json.dump(out, open('sim.json', 'w'))
for k, e in out['exact'].items(): print(k, {a: round(b, 4) for a, b in e.items()})
