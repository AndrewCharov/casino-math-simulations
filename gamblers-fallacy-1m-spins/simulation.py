# Gambler's Fallacy Tested: Is Red Ever Due? 1,000,000 Roulette Spins
# Full write-up with charts: https://boosterhand.com/lab/gamblers-fallacy-1-million-roulette-spins/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
import numpy as np, json
rng=np.random.default_rng(707)
N=1_000_000
# European wheel: 0 green, 18 red, 18 black
r=rng.integers(0,37,N)
RED={1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
col=np.array([0 if x==0 else (1 if x in RED else 2) for x in r])  # 1 red, 2 black, 0 green
out={'n':N,'red':float((col==1).mean()),'black':float((col==2).mean()),'green':float((col==0).mean())}
# after streaks of k blacks (non-red), probability next is red
res={}
for k in (1,3,5,8,10):
    # find positions where previous k spins were black
    b=(col==2).astype(np.int8)
    c=np.convolve(b,np.ones(k,int),'valid')  # c[i]=sum b[i..i+k-1]
    idx=np.where(c[:-1]==k)[0]+k  # next index
    idx=idx[idx<N]
    res[str(k)]={'count':int(len(idx)),'p_red':float((col[idx]==1).mean())}
out['after_black']=res
# longest streak of same color (red or black, green breaks)
best=cur=0;prev=-1
for x in col:
    if x!=0 and x==prev: cur+=1
    else: cur=1 if x!=0 else 0
    prev=x; best=max(best,cur)
out['longest']=best
# betting strategy: wait for 5 blacks then bet red $10, vs bet red every spin $10 — edge
b5=res['5']
out['wait5']={'bets':b5['count'],'win':b5['p_red'],'ret':b5['p_red']*2}
out['always']={'win':out['red'],'ret':out['red']*2}
json.dump(out,open('sim.json','w'),indent=1); print(json.dumps(out,indent=1))
