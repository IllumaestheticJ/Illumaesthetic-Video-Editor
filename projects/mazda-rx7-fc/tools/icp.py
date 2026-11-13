import numpy as np
from scipy.spatial import cKDTree
def icp(P, T, iters=40, trim=0.7, R=None, t=None):
    """rigid ICP of points P onto KD-tree T (trimmed). returns R,t, median residual"""
    R=np.eye(3) if R is None else R; t=np.zeros(3) if t is None else t
    for it in range(iters):
        Q=P@R.T+t; d,i=T.query(Q); keep=d<=np.quantile(d,trim)
        A=Q[keep]; B=T.data[i[keep]]
        ca,cb=A.mean(0),B.mean(0); H=(A-ca).T@(B-cb); U,S,Vt=np.linalg.svd(H)
        D=np.diag([1,1,np.sign(np.linalg.det(Vt.T@U.T))]); dR=Vt.T@D@U.T
        R=dR@R; t=dR@(t-ca)+cb
    d,_=T.query(P@R.T+t); return R,t,np.median(d),np.percentile(d,90)
