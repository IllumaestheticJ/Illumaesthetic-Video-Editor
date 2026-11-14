"""Quick orthographic depth splats of one or more STLs (top / side / front), for checking frames and registration.
usage: ortho.py out.png a.stl[:color] b.stl[:color] ... [--mm 6]"""
import sys, numpy as np
from PIL import Image
sys.path.insert(0, '/home/user/Illumaesthetic-Video-Editor')
def load(p):
    import struct
    with open(p,'rb') as f:
        f.read(80); n=struct.unpack('<I',f.read(4))[0]
        d=np.frombuffer(f.read(n*50),dtype=np.dtype([('n','<3f4'),('v','<9f4'),('a','<u2')]))
    return d['v'].reshape(-1,3,3).mean(1)
mm=6
argv=sys.argv[1:]
if '--mm' in argv: i=argv.index('--mm'); mm=float(argv[i+1]); del argv[i:i+2]
args=argv
out=args[0]; cols=[(200,200,200),(255,60,60),(60,160,255),(80,255,80),(255,200,0),(255,0,255)]
sets=[]
for i,a in enumerate(args[1:]):
    p=a.split(':')[0]; sets.append((load(p),cols[i%len(cols)]))
allp=np.concatenate([s[0] for s in sets]); lo=allp.min(0); hi=allp.max(0)
print('bbox lo',lo.round(0),'hi',hi.round(0),'size',(hi-lo).round(0))
views=[(0,1,2),(0,2,1),(1,2,0)]  # (u,v,depth): XY top, XZ, YZ
tiles=[]
for u,v,dax in views:
    W=int((hi[u]-lo[u])/mm)+1; H=int((hi[v]-lo[v])/mm)+1
    img=np.zeros((H,W,3),np.uint8); dep=np.full((H,W),-1e9)
    for pts,c in sets:
        iu=((pts[:,u]-lo[u])/mm).astype(int); iv=(H-1-((pts[:,v]-lo[v])/mm)).astype(int)
        d=pts[:,dax]
        o=np.argsort(d); iu,iv,d=iu[o],iv[o],d[o]
        dep[iv,iu]=d
        shade=(0.35+0.65*(d-lo[dax])/(hi[dax]-lo[dax]+1e-9))[:,None]
        img[iv,iu]=(np.array(c)[None]*shade).astype(np.uint8)
    tiles.append(img)
Hm=sum(t.shape[0] for t in tiles)+20; Wm=max(t.shape[1] for t in tiles)
canvas=np.zeros((Hm,Wm,3),np.uint8); y=0
for t in tiles: canvas[y:y+t.shape[0],:t.shape[1]]=t; y+=t.shape[0]+10
Image.fromarray(canvas).save(out); print(out, canvas.shape)
