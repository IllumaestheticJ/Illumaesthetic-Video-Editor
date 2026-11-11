"""Rough camera solve of the GT-wing listing photo (rear-quarter-white, worked at 1288x725) on the configurator's own DE5 model.
Landmarks picked on a reference render (ref px -> 3D by ray pick) and on the photo; focal swept, EPNP + LM."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from rast import *
import json
W,H=1288,725
V,F,C=load(('car',)); R,t=lookat((-3.2,1.7,-3.6),(1.6,0.7,0))
img,idm=render(V,F,C,R,t,1500,W,H,ids=True)
ref={'emblem':(920,368),'plate':(935,465),'wheel_rl':(540,525),'wheel_fl':(232,410),'mirror_l':(285,280),'handle_r':(487,362),'handle_f':(360,338),'fin':(700,207)}
pho={'emblem':(1028,318),'plate':(1045,428),'wheel_rl':(612,497),'wheel_fl':(268,373),'mirror_l':(325,262),'handle_r':(553,338),'handle_f':(405,313),'fin':(722,163)}
O=[];I=[];N=[]
for k,px in ref.items():
    X=pick(V,F,R,t,1500,W,H,idm,px); print(k,None if X is None else X.round(3))
    if X is not None: O.append(X); I.append(pho[k]); N.append(k)
O=np.array(O);I=np.array(I,float); best=None
for f in (700,800,900,1000,1100,1250,1400,1600):
    K=np.array([[f,0,W/2],[0,f,H/2],[0,0,1.]])
    ok,r,tv=cv2.solvePnP(O,I,K,None,flags=cv2.SOLVEPNP_EPNP)
    r,tv=cv2.solvePnPRefineLM(O,I,K,None,r,tv)
    q,_=cv2.projectPoints(O,r,tv,K,None); e=np.linalg.norm(q.reshape(-1,2)-I,axis=1)
    Rm,_=cv2.Rodrigues(r); eye=(-Rm.T@tv).ravel(); rm=float(np.sqrt((e**2).mean())); print(f,round(rm,1),e.round(0),eye.round(2))
    json.dump({'f':f,'rvec':r.ravel().tolist(),'tvec':tv.ravel().tolist(),'w':W,'h':H},open(f'cam0_{f}.json','w'))
