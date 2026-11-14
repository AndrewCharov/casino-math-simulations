# I Dropped 1,000,000 Plinko Balls: Plinko Odds, RTP and Risk Levels Simulated
# Full write-up with charts: https://boosterhand.com/lab/plinko-simulation-1-million-balls/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
import numpy as np, json
from math import comb
rng=np.random.default_rng(1515)
R=16; C=np.array([comb(R,k) for k in range(R+1)]); P=C/2**R
def sym(h): return np.array(h+h[-2::-1],float)  # 9 half values -> 17 slots
T={'low':sym([16,9,2,1.4,1.4,1.2,1.1,1,0.5]),
   'medium':sym([110,41,10,5,3,1.5,1,0.5,0.3]),
   'high':sym([1000,130,26,9,4,2,0.2,0.2,0.2])}
out={'rows':R,'counts':C.tolist(),'probs':P.tolist(),'p_edge_slot_each':1/2**R,'p_max_either_edge':2/2**R,'balls_per_max_hit':2**R/2}
N=1_000_000; NP=10_000; NB=1_000
for name,m in T.items():
    ev=float((P*m).sum()); sd=float(np.sqrt((P*(m-ev)**2).sum()))
    slots=rng.binomial(R,0.5,N); pay=m[slots]
    hist=np.bincount(slots,minlength=R+1)
    cum=np.cumsum(pay-1.0)
    curve=cum[np.linspace(0,N-1,201).astype(int)].round(2).tolist()
    # players
    res=np.zeros(NP); hm=np.zeros(NP,bool)
    for i in range(0,NP,1000):
        s=rng.binomial(R,0.5,(1000,NB)); res[i:i+1000]=m[s].sum(1)-NB; hm[i:i+1000]=((s==0)|(s==R)).any(1)
    out[name]={'table':m.tolist(),'rtp_exact':ev,'rtp_exact_fraction':f"{int(round((C*m).sum()*10))}/{2**R*10}",'sd_per_ball':sd,
      'p_ball_returns_less_than_bet':float(P[m<1].sum()),'p_ball_profit':float(P[m>1].sum()),
      'm1':{'wagered':N,'returned':float(pay.sum()),'net':float(pay.sum()-N),'rtp_sim':float(pay.mean()),'hist':hist.tolist(),
            'max_hits':int(hist[0]+hist[R]),'first_max_ball':int(np.argmax((slots==0)|(slots==R))+1),'curve':curve,
            'worst_running':float(cum.min()),'best_running':float(cum.max())},
      'players':{'share_up':float((res>0).mean()),'share_even_or_up':float((res>=0).mean()),'median':float(np.median(res)),'mean':float(res.mean()),
            'worst':float(res.min()),'best':float(res.max()),'p10':float(np.percentile(res,10)),'p90':float(np.percentile(res,90)),
            'share_lost_100plus':float((res<=-100).mean()),'share_hit_max':float(hm.mean()),
            'hist10':np.histogram(np.clip(res,-349.9,449.9),bins=np.arange(-350,451,10))[0].tolist(),'over450':int((res>450).sum()),'hist_edges':np.percentile(res,[1,5,25,50,75,95,99]).round(1).tolist()}}
json.dump(out,open('sim.json','w'),indent=1)
for name in T:
    o=out[name];print(name,o['table'][:9],'RTP',round(o['rtp_exact'],5),'sd',round(o['sd_per_ball'],2),'pLess',round(o['p_ball_returns_less_than_bet'],4))
    print('  1M:',{k:v for k,v in o['m1'].items() if k not in('curve','hist')})
    print('  players:',o['players'])
