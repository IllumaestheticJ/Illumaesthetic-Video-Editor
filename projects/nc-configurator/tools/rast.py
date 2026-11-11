"""tiny painter's rasteriser for the exported configurator scene (metres; x fwd from rear bumper, y up, z side)"""
import numpy as np, cv2
def load(names=('car','kit')):
    V=[];F=[];C=[];o=0
    for n in names:
        m=np.load(f'/home/user/media/work/nc/match/{n}.npz'); V.append(m['v']);F.append(m['f']+o);C.append(m['c']);o+=len(m['v'])
    return np.vstack(V),np.vstack(F),np.concatenate(C)
def lookat(eye,target,up=(0,1,0)):
    eye=np.array(eye,float);z=np.array(target,float)-eye;z/=np.linalg.norm(z)
    x=np.cross(z,up);x/=np.linalg.norm(x);y=np.cross(z,x)   # opencv: x right, y down, z fwd
    R=np.stack([x,y,z]);return R,-R@eye
def render(V,F,C,R,t,f,w,h,cx=None,cy=None,ids=False):
    cx=w/2 if cx is None else cx; cy=h/2 if cy is None else cy
    P=V@R.T+t; z=P[:,2]; uv=np.c_[f*P[:,0]/z+cx,f*P[:,1]/z+cy]
    tz=z[F]; ok=(tz>0.05).all(1); d=tz.mean(1)
    n=np.cross(P[F[:,1]]-P[F[:,0]],P[F[:,2]]-P[F[:,0]]); n/=np.linalg.norm(n,axis=1)[:,None]+1e-12
    sh=0.35+0.65*np.abs(n[:,2])
    order=np.argsort(-d); img=np.full((h,w,3),240,np.uint8); idm=np.full((h,w),-1,np.int32)
    for i in order:
        if not ok[i]: continue
        p=np.round(uv[F[i]]*16).astype(np.int32)
        if ids: cv2.fillConvexPoly(idm,p,int(i),shift=4)
        c=C[i]; col=np.array([c&255,(c>>8)&255,(c>>16)&255])*sh[i]
        cv2.fillConvexPoly(img,p,col.tolist(),shift=4,lineType=cv2.LINE_AA)
    return (img,idm) if ids else img
def pick(V,F,R,t,f,w,h,idm,px,cx=None,cy=None):
    cx=w/2 if cx is None else cx; cy=h/2 if cy is None else cy
    i=idm[int(px[1]),int(px[0])]
    if i<0: return None
    a,b,c=V[F[i]]; n=np.cross(b-a,c-a); o=-R.T@t; dr=R.T@np.array([(px[0]-cx)/f,(px[1]-cy)/f,1.0])
    s=((a-o)@n)/(dr@n); return o+s*dr
