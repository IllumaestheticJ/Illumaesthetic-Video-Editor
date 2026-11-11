"""v2 camera solve: Drive photo _DSF3972 (7145x4763, worked at 1429x953) on the configurator's DE5 model. Landmarks picked on a reference render
(ray pick -> 3D) and on the photo; long lens, so focal is swept and the solve starts from the reference camera (useExtrinsicGuess)."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from rast import *
import json
W,H=1429,953
V,F,C=load(('car',)); R,t=lookat((-6.5,1.5,4.2),(1.6,0.75,0)); F0=3000
img,idm=render(V,F,C,R,t,F0,W,H,ids=True)
d=lambda x,y:(200+x/1.8,280+y/1.8)   # grid-image px -> 1429-scale px
ref={'emblem':d(445,340),'plate':d(430,568),'wheel_rr':d(1262,690),'wheel_fr':d(1845,560),'mirror_r':d(1710,190),'handle_r':d(1345,345),'handle_f':d(1570,325),'exhaust':d(470,755)}
pho={'emblem':(470,497),'plate':(465,597),'wheel_rr':(832,650),'wheel_fr':(1095,625),'mirror_r':(1018,435),'handle_r':(855,502),'handle_f':(950,495),'exhaust':(470,680)}   # 1429-scale px (first pass had the front handle labelled as the rear one)
O=[];I=[];N=[]
for k,px in ref.items():
    X=pick(V,F,R,t,F0,W,H,idm,px); print(k,None if X is None else X.round(3))
    if X is not None: O.append(X); I.append(pho[k]); N.append(k)
O=np.array(O);I=np.array(I,float); r0,_=cv2.Rodrigues(R)
for f in (1500,2000,2500,3000,3500,4000,5000,6500):
    K=np.array([[f,0,W/2],[0,f,H/2],[0,0,1.]])
    ok,r,tv=cv2.solvePnP(O,I,K,None,r0.copy(),(t*f/F0).reshape(3,1).copy()*np.array([[1],[1],[1.]]),useExtrinsicGuess=True,flags=cv2.SOLVEPNP_ITERATIVE)
    q,_=cv2.projectPoints(O,r,tv,K,None); e=np.linalg.norm(q.reshape(-1,2)-I,axis=1)
    Rm,_=cv2.Rodrigues(r); eye=(-Rm.T@tv).ravel(); print(f,round(float(np.sqrt((e**2).mean())),1),e.round(0),eye.round(2))
    json.dump({'f':f,'rvec':r.ravel().tolist(),'tvec':tv.ravel().tolist(),'w':W,'h':H},open(f'cam_v2_{f}.json','w'))
json.dump({'points':[{'name':n,'xyz':o.tolist(),'px':list(i)} for n,o,i in zip(N,O,I)]},open('points_v2.json','w'))
