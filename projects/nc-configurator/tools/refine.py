import sys; sys.path.insert(0,'.')
from rast import *
import json
from scipy.optimize import minimize
PH=sys.argv[1]; cin=sys.argv[2]; cout=sys.argv[3]; fixf='--fix-f' in sys.argv
img=cv2.imread(PH); H0,W0=img.shape[:2]; w=750; s=w/W0; h=int(round(H0*s)); small=cv2.resize(img,(w,h),interpolation=cv2.INTER_AREA)
hsv=cv2.cvtColor(small,cv2.COLOR_BGR2HSV)
pink=((hsv[...,0]>=140)&(hsv[...,0]<=178)&(hsv[...,1]>70)&(hsv[...,2]>50)).astype(np.uint8)*255
pink=cv2.morphologyEx(pink,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); pink=cv2.morphologyEx(pink,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(pink); pink=np.where(lab==1+np.argmax(st[1:,4]),255,0).astype(np.uint8)
cs,_=cv2.findContours(pink,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); pm=np.zeros_like(pink); cv2.drawContours(pm,cs,-1,255,-1)
V,F,C=load(('car',)); body=C==0xd9d9d9; Fb=F[body]
cam=json.load(open(cin)); r0=np.array(cam['rvec']);t0=np.array(cam['tvec']);f0=cam['f']*w/cam['w']
keep=np.ones((h,w),bool); keep[:6]=0;keep[-6:]=0;keep[:,:6]=0;keep[:,-6:]=0
for b in [a for a in sys.argv if a.startswith('--ignore=')]:
    for box in b[9:].split(';'):
        x0,y0,x1,y1=[int(v) for v in box.split(',')]; keep[y0:y1,x0:x1]=0
edge=lambda m: cv2.morphologyEx(m,cv2.MORPH_GRADIENT,np.ones((3,3),np.uint8))>0
pe=edge(pm)&keep; dt_p=cv2.distanceTransform((~pe).astype(np.uint8),cv2.DIST_L2,3); pys,pxs=np.nonzero(pe)
def sil(r,t,f):
    K=np.array([[f,0,w/2],[0,f,h/2],[0,0,1.]]); p,_=cv2.projectPoints(V,r,t,K,None); p=np.round(p.reshape(-1,2)*4).astype(np.int32)
    m=np.zeros((h,w),np.uint8); cv2.fillPoly(m,list(p[Fb]),255,shift=2); m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); o=np.zeros_like(m); cv2.drawContours(o,cs,-1,255,-1); return o
T=15
def unpack(x): return r0+x[:3]*0.01,t0+x[3:6]*0.02,f0*np.exp(0 if fixf else x[6]*0.02)
def cost(x,v=False):
    r,t,f=unpack(x); m=sil(r,t,f); re=edge(m)&keep; ys,xs=np.nonzero(re)
    if len(xs)<50: return 1e3
    d1=np.minimum(dt_p[ys,xs],T).mean(); dt_r=cv2.distanceTransform((~re).astype(np.uint8),cv2.DIST_L2,3); d2=np.minimum(dt_r[pys,pxs],T).mean()
    if v: print(f'chamfer {d1:.2f} {d2:.2f}')
    return d1+d2
x=np.zeros(7); cost(x,True)
for it in range(2):
    x=minimize(cost,x,method='Powell',options={'maxiter':3000,'xtol':1e-3,'ftol':1e-4}).x
x=minimize(cost,x,method='Nelder-Mead',options={'maxiter':1500}).x; cost(x,True)
r,t,f=unpack(x); Rm,_=cv2.Rodrigues(r); eye=(-Rm.T@t).ravel(); print('f',f,'eye',eye.round(3))
json.dump({'f':f,'rvec':r.tolist(),'tvec':t.tolist(),'w':w,'h':h},open(cout,'w'))
vis=small.copy(); vis[pe]=(0,160,255); vis[edge(sil(r,t,f))]=(255,255,0); cv2.imwrite(cout.replace('.json','.refine.jpg'),vis)
# onion: full scene render blended on photo
Va,Fa,Ca=load(); K=np.array([[f,0,w/2],[0,f,h/2],[0,0,1.]]); ren=render(Va,Fa,Ca,Rm,t,f,w,h)
msk=(ren!=240).any(2)[...,None]; on=np.where(msk,(0.5*small+0.5*ren).astype(np.uint8),small); cv2.imwrite(cout.replace('.json','.onion.jpg'),on)
