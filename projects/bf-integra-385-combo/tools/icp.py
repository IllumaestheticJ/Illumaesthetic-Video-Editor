# rigid ICP scan -> GLB frame, multi-start over yaw; writes 4x4 (applied to scan world coords)
import numpy as np, json, sys
from scipy.spatial import cKDTree
S=np.load(sys.argv[1]); G=np.load(sys.argv[2]); out=sys.argv[3]
rng=np.random.default_rng(1); S=S[rng.choice(len(S),60000,replace=False)]; Gs=G
tree=cKDTree(Gs)
def best_fit(A,B):
    ca,cb=A.mean(0),B.mean(0); H=(A-ca).T@(B-cb); U,_,Vt=np.linalg.svd(H); R=Vt.T@U.T
    if np.linalg.det(R)<0: Vt[-1]*=-1; R=Vt.T@U.T
    return R, cb-R@ca
def icp(T,iters=40,trim=0.8):
    for it in range(iters):
        X=S@T[:3,:3].T+T[:3,3]; d,i=tree.query(X); k=d<np.quantile(d,trim)
        R,t=best_fit(X[k],Gs[i[k]]); D=np.eye(4); D[:3,:3]=R; D[:3,3]=t; T=D@T
    X=S@T[:3,:3].T+T[:3,3]; d,_=tree.query(X); return T,np.median(d)
res=[]
for yaw in np.arange(0,360,20):
    a=np.radians(yaw); R=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
    T=np.eye(4); T[:3,:3]=R; T[:3,3]=G.mean(0)-R@S.mean(0)
    T,e=icp(T); res.append((e,yaw,T))
res.sort(key=lambda r:r[0]); print([(round(e*1000,1),y) for e,y,_ in res[:6]])
T,e=icp(res[0][2],60,0.9); print('final median mm',e*1000)
json.dump({'matrix':T.tolist(),'median_mm':e*1000},open(out,'w'))
