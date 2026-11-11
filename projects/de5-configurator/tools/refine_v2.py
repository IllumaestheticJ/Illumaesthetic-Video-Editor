"""Refine the v2 camera: maximise silhouette IoU (car + kit vs GrabCut mask of the photo, shadow zone ignored) plus a landmark term, Nelder-Mead on rvec, tvec, log f.
Works at half of the 1429x953 working size."""
import sys, os, json; sys.path.insert(0, os.path.dirname(__file__))
from rast import *
from scipy.optimize import minimize
cam=json.load(open('cam_v2_4000.json')); P=json.load(open('points_v2.json'))['points']; mask=np.load('mask_v2.npy').astype(bool); h,w=mask.shape
V,F,C=load(); O=np.array([p['xyz'] for p in P]); I=np.array([p['px'] for p in P])/2
ign=np.zeros_like(mask); ign[292:]=True                      # tyres' contact / shadow under the car
def sil(x):
    R,_=cv2.Rodrigues(x[:3]); f=np.exp(x[6]); Pc=V@R.T+x[3:6]; uv=np.c_[f*Pc[:,0]/Pc[:,2]+w/2,f*Pc[:,1]/Pc[:,2]+h/2]
    m=np.zeros((h,w),np.uint8); cv2.fillPoly(m,list(np.round(uv[F]).astype(np.int32)),1); return m.astype(bool)
def cost(x,parts=False):
    m=sil(x); a=m&~ign; b=mask&~ign; iou=(a&b).sum()/max(1,(a|b).sum())
    R,_=cv2.Rodrigues(x[:3]); f=np.exp(x[6]); q=O@R.T+x[3:6]; q=np.c_[f*q[:,0]/q[:,2]+w/2,f*q[:,1]/q[:,2]+h/2]; e=np.sqrt(((q-I)**2).sum(1).mean())
    return (iou,e) if parts else (1-iou)+e/150
x0=np.r_[cam['rvec'],cam['tvec'],np.log(cam['f']/2)]; print('start',cost(x0,True))
r=minimize(cost,x0,method='Nelder-Mead',options={'maxiter':900,'xatol':1e-4,'fatol':1e-5,'initial_simplex':x0+np.vstack([np.zeros(7),np.diag([.01,.01,.01,.05,.05,.3,.05])])})
x=r.x; print('end',cost(x,True),'f',np.exp(x[6])*2); Rm,_=cv2.Rodrigues(x[:3]); print('eye',(-Rm.T@x[3:6]).round(2))
json.dump({'f':float(np.exp(x[6])*2),'rvec':x[:3].tolist(),'tvec':x[3:6].tolist(),'w':1429,'h':953},open('cam_v2.json','w'))
