# Betting Systems Tested on 70,000 Players: Which One Fails Fastest?
# Full write-up with charts: https://boosterhand.com/lab/betting-systems-tested-70000-players/
# Run: python simulation.py   (writes sim.json, prints a summary)
# MIT licence. Generic game model, not any specific casino or game.
# 7 betting systems on even-money European roulette (p=18/37). Generic model.
import numpy as np, json
p=18/37; BANK=1000; BASE=10; LIMIT=1000; M=10000; S=1000
def sim(name, seed):
    rng=np.random.default_rng(seed)
    bal=np.full(M,float(BANK)); alive=np.ones(M,bool); wag=np.zeros(M); bust=np.full(M,-1)
    unit=np.full(M,float(BASE)); streak=np.zeros(M,int); fa=np.zeros(M,int); fb=np.zeros(M,int)  # fib idx
    lab=[[1,2,3,4] for _ in range(M)] if name=='Labouchere' else None
    sess=np.zeros(M)  # oscar session profit
    fib=[1,1]
    while len(fib)<60: fib.append(fib[-1]+fib[-2])
    fib=np.array(fib,float)
    path=[]; snaps={}
    for s in range(1,S+1):
        if name=='Flat': bet=np.full(M,BASE*1.0)
        elif name=='Martingale': bet=unit.copy()
        elif name=='Fibonacci': bet=BASE*fib[np.minimum(fa,59)]
        elif name=="D'Alembert": bet=unit.copy()
        elif name=='Paroli': bet=unit.copy()
        elif name=="Oscar's Grind": bet=unit.copy()
        elif name=='Labouchere': bet=np.array([BASE*((l[0]+l[-1]) if len(l)>1 else l[0]) if l else BASE for l in lab],float)
        bet=np.minimum(bet,LIMIT); bet=np.minimum(bet,bal); act=alive&(bet>0)
        w=rng.random(M)<p
        wag[act]+=bet[act]; d=np.where(w,bet,-bet); bal[act]+=d[act]
        # update rules
        if name=='Martingale': unit=np.where(w,BASE,unit*2); unit[unit>LIMIT]=BASE
        elif name=='Fibonacci': fa=np.where(w,np.maximum(fa-2,0),fa+1)
        elif name=="D'Alembert": unit=np.where(w,np.maximum(unit-BASE,BASE),unit+BASE)
        elif name=='Paroli':
            streak=np.where(w,streak+1,0); unit=np.where(w&(streak<3),unit*2,BASE); streak[streak>=3]=0
        elif name=="Oscar's Grind":
            sess+=np.where(act,d,0)
            reach=sess>=BASE; sess[reach]=0; unit[reach]=BASE
            inc=w&~reach; unit[inc]=np.minimum(unit[inc]+BASE, np.maximum(BASE, BASE-sess[inc]))
        elif name=='Labouchere':
            for i in np.where(act)[0]:
                l=lab[i]
                if w[i]:
                    if len(l)>1: l.pop(0); l.pop(-1)
                    else: l.clear()
                    if not l: lab[i]=[1,2,3,4]
                else: l.append(int(bet[i]/BASE))
        died=alive&(bal<BASE); bust[died]=s; alive&=~died
        if s%10==0: path.append(float(np.median(bal)))
        if s in (100,250,500,1000): snaps[s]={'ahead':float((bal>BANK).mean()),'broke':float((~alive).mean())}
    return {'name':name,'broke':float((~alive).mean()),'ahead':float((bal>BANK).mean()),'avg':float(bal.mean()),'median':float(np.median(bal)),
      'avg_loss':float(BANK-bal.mean()),'wag':float(wag.mean()),'edge':float((BANK-bal.mean())/wag.mean()),
      'median_bust':float(np.median(bust[bust>0])) if (bust>0).any() else None,'snaps':snaps,'path':path}
R=[sim(n,i+11) for i,n in enumerate(['Flat','Martingale','Fibonacci',"D'Alembert",'Labouchere','Paroli',"Oscar's Grind"])]
json.dump(R,open('sim.json','w'))
for r in R: print(f"{r['name']:14s} broke {r['broke']*100:5.1f}% ahead {r['ahead']*100:5.1f}% avg {r['avg']:7.1f} med {r['median']:7.1f} wag {r['wag']:8.0f} edge {r['edge']*100:.2f}% medbust {r['median_bust']}")
