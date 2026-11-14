# RTP Explained: What 96% RTP Really Means for Your $100
# Full write-up with charts: https://boosterhand.com/lab/rtp-explained-96-percent-simulation/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
import numpy as np, json
rng=np.random.default_rng(404)
MULT=np.array([0,0.5,1,2,3,5,10,20,50,100,250,1000,5000],float)
P0=np.array([0,.10,.07,.06,.045,.028,.0105,.003,.0012,.0004,.0001,.00002,.000003])
def table(rtp):
    P=P0.copy(); P[3]+= (rtp-(P*MULT).sum())/MULT[3]; P[0]=1-P[1:].sum(); return P
out={}
P96=table(0.96)
# session RTP spread for 10,000 sessions at different lengths
spread={}
for n in (100,1000,10000,100000):
    k=10000 if n<=10000 else 2000
    tot=np.zeros(k)
    left=n
    while left>0:
        c=min(left,2000); tot+=rng.choice(MULT,size=(k,c),p=P96).sum(1); left-=c
    r=tot/n
    spread[n]={'p5':float(np.percentile(r,5)),'p50':float(np.median(r)),'p95':float(np.percentile(r,95)),'above100':float((r>1).mean())}
# 1M spins x 200 sessions approximate via normal (var per spin)
var=(P96*MULT**2).sum()-0.96**2; sd=np.sqrt(var/1e6)
spread[1000000]={'p5':0.96-1.645*sd,'p50':0.96,'p95':0.96+1.645*sd,'above100':0.0}
out['spread']=spread
# bankroll lasting: $100, $1 spins, until broke (max 20000), for rtp 0.96,0.94,0.92,0.88
last={}
for rtp in (0.96,0.94,0.92,0.88):
    P=table(rtp); M=10000; bal=np.full(M,100.0); alive=np.ones(M,bool); bust=np.full(M,20000); s=0
    while alive.any() and s<20000:
        s+=1; w=rng.choice(MULT,size=M,p=P); bal[alive]+=w[alive]-1; d=alive&(bal<1); bust[d]=s; alive&=~d
    last[str(rtp)]={'median':float(np.median(bust)),'mean':float(bust.mean()),'hour_loss_600':600*(1-rtp)}
out['last']=last
json.dump(out,open('sim.json','w'),indent=1); print(json.dumps(out,indent=1))
