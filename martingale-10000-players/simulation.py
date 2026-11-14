# Martingale Strategy Tested on 10,000 Players: Does It Really Work?
# Full write-up with charts: https://boosterhand.com/lab/martingale-strategy-simulation-10000-players/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
# Martingale on even-money roulette bets (European wheel, p(win)=18/37). Generic model.
import numpy as np, json
rng=np.random.default_rng(777); p=18/37
out={'p':p}
def run(M,S,bank,base,limit,goal=None):
    bal=np.full(M,float(bank)); bet=np.full(M,float(base)); alive=np.ones(M,bool); done=np.zeros(M,bool)
    wag=np.zeros(M); peak=bal.copy(); bust_at=np.full(M,-1); maxstreak=np.zeros(M,int); cur=np.zeros(M,int)
    snaps={}
    for s in range(1,S+1):
        act=alive&~done
        if not act.any(): break
        # can't cover the next bet or above table limit -> reset to base if possible, else bust
        over=act&(bet>limit); bet[over]=base
        cant=act&(bet>bal)
        bet[cant]=np.minimum(bal[cant],bet[cant])  # all-in with what's left
        w=rng.random(M)<p
        wag[act]+=bet[act]
        bal[act&w]+=bet[act&w]; bal[act&~w]-=bet[act&~w]
        cur[act&~w]+=1; cur[act&w]=0; maxstreak=np.maximum(maxstreak,cur)
        bet[act&w]=base; bet[act&~w]*=2
        peak=np.maximum(peak,bal)
        b=act&(bal<base); bust_at[b]=s; alive&=~b
        if goal is not None: done|=act&(bal>=bank+goal)
        if s in (10,50,100,250,500,1000): snaps[s]={'ahead':float((bal>bank).mean()),'bust':float((~alive).mean()),'avg':float(bal.mean()),'median':float(np.median(bal))}
    return bal,wag,peak,bust_at,maxstreak,snaps,done
# A) one player path: bank 1000, base 10, table limit 1000, 1000 spins
bal1,_,_,_,_,_,_=None,None,None,None,None,None,None
M,S=10000,1000
bal,wag,peak,bust,ms,snaps,_=run(M,S,1000,10,1000)
out['B']={'snaps':snaps,'ahead':float((bal>1000).mean()),'bust':float((bust>0).mean()),'avg':float(bal.mean()),'median':float(np.median(bal)),
 'avg_loss':float(1000-bal.mean()),'wagered_avg':float(wag.mean()),'edge_check':float((1000-bal.mean())/wag.mean()),
 'median_bust_spin':float(np.median(bust[bust>0])) if (bust>0).any() else None,
 'ever_up_200':float((peak>=1200).mean()),'hist':np.histogram(bal,bins=[0,10,500,900,1000,1100,1300,2000,1e9])[0].tolist(),
 'maxstreak_dist':{str(k):float((ms>=k).mean()) for k in range(5,15)}}
# pick a sample player who goes up steadily then crashes
# re-simulate single players until one busts after being up
def one(seed):
    r=np.random.default_rng(seed); b=1000.0; bet=10.0; path=[b]
    for s in range(1000):
        if bet>1000: bet=10
        bet=min(bet,b)
        if r.random()<p: b+=bet; bet=10
        else: b-=bet; bet*=2
        path.append(b)
        if b<10: break
    return path
best=None
for sd in range(5000):
    pa=one(sd)
    if len(pa)>350 and pa[-1]<10 and max(pa)>1250: best=(sd,pa); break
out['A']={'seed':best[0],'path':[round(x,1) for x in best[1]],'peak':max(best[1]),'peak_at':int(np.argmax(best[1])),'len':len(best[1])-1}
# C) goal variant: stop at +$100
bal2,wag2,_,bust2,_,_,done2=run(M,5000,1000,10,1000,goal=100)
out['C']={'reached':float(done2.mean()),'bust':float((bust2>0).mean()),'avg':float(bal2.mean()),'avg_loss':float(1000-bal2.mean())}
# D) streak probability in 1000 spins analytic-ish via sim
L=rng.random((20000,1000))>=p
def longest(row):
    m=c=0
    for v in row:
        c=c+1 if v else 0; m=max(m,c)
    return m
lg=np.array([longest(r) for r in L[:4000]])
out['D']={str(k):float((lg>=k).mean()) for k in range(6,13)}
out['ladder']=[10*2**i for i in range(11)]
json.dump(out,open('sim.json','w'))
print(json.dumps({k:v for k,v in out['B'].items()},indent=0)); print(out['C']); print(out['D']); print('A',out['A']['seed'],out['A']['peak'],out['A']['peak_at'],out['A']['len'])
