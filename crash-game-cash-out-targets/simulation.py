# Crash Game Strategy: When Should You Cash Out? 60,000 Players Tested
# Full write-up with charts: https://boosterhand.com/lab/crash-game-cash-out-strategy-simulation/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
import numpy as np, json
# Generic crash game, 1% house edge: P(M >= x) = 0.99/x for x>=1 (about 1% instant crash at 1.00x)
rng=np.random.default_rng(1212)
TARGETS=[1.1,1.5,2,5,10,100]
N=10000; BANK=100.0; ROUNDS=1000
out={'edge':0.01,'players':N,'bank':BANK,'rounds':ROUNDS,'targets':{}}
for x in TARGETS:
    bal=np.full(N,BANK); alive=np.ones(N,bool); bust=np.full(N,ROUNDS+1); peak=bal.copy()
    wins=0; bets=0; wag=0.0; ret=0.0; snap={}
    for r in range(1,ROUNDS+1):
        u=1.0-rng.random(N)            # (0,1]
        M=np.maximum(1.0,0.99/u)       # P(M>=x)=0.99/x
        M=np.floor(M*100)/100          # displayed to 2 decimals
        win=(M>=x)&alive
        nb=alive.sum(); bets+=nb; wins+=win.sum(); wag+=nb; ret+=win.sum()*x
        bal[alive]-=1; bal[win]+=x
        peak=np.maximum(peak,bal)
        d=alive&(bal<1); bust[d]=r; alive&=~d
        if r in (100,300,1000): snap[r]={'broke':float((~alive).mean()),'median':float(np.median(bal)),'ahead':float((bal>BANK).mean())}
    out['targets'][str(x)]={'theory_win':0.99/x,'win_rate':float(wins/bets),'return_per_dollar':float(ret/wag),
      'broke':float((~alive).mean()),'median_rounds':float(np.median(np.minimum(bust,ROUNDS))),
      'ever_double':float((peak>=200).mean()),'max_balance':float(peak.max()),'max_final':float(bal.max()),
      'median_final':float(np.median(bal)),'ahead_end':float((bal>BANK).mean()),'snap':snap,'bets':int(bets)}
json.dump(out,open('sim.json','w'),indent=1)
for k,v in out['targets'].items(): print(k,{a:(round(b,4) if isinstance(b,float) else b) for a,b in v.items() if a!='snap'},v['snap'])
