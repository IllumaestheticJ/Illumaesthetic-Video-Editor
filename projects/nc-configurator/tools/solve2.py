import sys; sys.path.insert(0,'.')
from rast import *
import json
cam=json.load(open('cam1.json')); V,F,C=load(('car',)); R,_=cv2.Rodrigues(np.array(cam['rvec'])); t=np.array(cam['tvec']); f=cam['f']
img,idm=render(V,F,C,R,t,f,750,1000,ids=True)
c=lambda x,y:(x/2+100,y/2+250)
pairs={'emblem':(c(755,405),c(840,395)),'plate':(c(752,500),c(820,495)),'tail_l':(c(385,560),c(510,525)),'tail_r':(c(925,430),c(980,410)),
       'marker':(c(300,690),c(350,675)),'fuel':(c(230,440),c(290,400)),'wheel':(c(85,690),(128,605))}
O=[];I=[];N=[]
for k,(m,p) in pairs.items():
    X=pick(V,F,R,t,f,750,1000,idm,m); print(k,None if X is None else X.round(3)); 
    if X is not None: O.append(X);I.append(p);N.append(k)
O=np.array(O);I=np.array(I,float)
res=[]
for f2 in (600,722,850,1000,1200,1500):
    K=np.array([[f2,0,375],[0,f2,500],[0,0,1.]])
    r,tv=cv2.solvePnPRefineLM(O,I,K,None,np.array(cam['rvec']).reshape(3,1),t.reshape(3,1).copy())
    q,_=cv2.projectPoints(O,r,tv,K,None); e=np.linalg.norm(q.reshape(-1,2)-I,axis=1)
    Rm,_=cv2.Rodrigues(r); print(f2,e.round(1),round(float(np.sqrt((e**2).mean())),1),(-Rm.T@tv).ravel().round(2))
    json.dump({'f':f2,'rvec':r.ravel().tolist(),'tvec':tv.ravel().tolist(),'w':750,'h':1000},open(f'cam2_{f2}.json','w'))
json.dump({'points':[{'name':n,'xyz':o.tolist(),'px':i.tolist()} for n,o,i in zip(N,O,I)]},open('points.json','w'))
