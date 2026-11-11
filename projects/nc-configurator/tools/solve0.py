import sys; sys.path.insert(0,'.')
from rast import *
import json
V,F,C=load(('car',)); R,t=lookat((-2.6,1.35,-2.0),(0.7,0.65,-0.1))
img,idm=render(V,F,C,R,t,900,750,1000,ids=True)
ref={'tail_l':(345,540),'plate':(473,522),'emblem':(478,485),'wheel_rl':(215,640),'tail_r':(560,508),'fuel':(268,470),'roof_top':(300,372)}
pho={'tail_l':(355,510),'plate':(511,492),'emblem':(521,446),'wheel_rl':(128,605),'tail_r':(592,455),'fuel':(243,448),'roof_top':(230,283)}
O=[];I=[]
for k,px in ref.items():
    X=pick(V,F,R,t,900,750,1000,idm,px); print(k,None if X is None else X.round(3))
    if X is not None: O.append(X); I.append(pho[k])
O=np.array(O);I=np.array(I,float)
best=None
for f in (500,560,620,680,722,800,900,1050):
    K=np.array([[f,0,375],[0,f,500],[0,0,1.]])
    ok,r,tv=cv2.solvePnP(O,I,K,None,flags=cv2.SOLVEPNP_EPNP)
    r,tv=cv2.solvePnPRefineLM(O,I,K,None,r,tv)
    q,_=cv2.projectPoints(O,r,tv,K,None); e=np.sqrt(((q.reshape(-1,2)-I)**2).sum(1).mean())
    Rm,_=cv2.Rodrigues(r); eye=(-Rm.T@tv).ravel(); print(f,round(e,1),eye.round(2))
    if best is None or e<best[0]: best=(e,f,r,tv)
e,f,r,tv=best
json.dump({'f':f,'rvec':r.ravel().tolist(),'tvec':tv.ravel().tolist(),'w':750,'h':1000},open('cam0.json','w'))
