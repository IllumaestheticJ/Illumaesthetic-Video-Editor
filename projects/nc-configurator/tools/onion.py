import sys; sys.path.insert(0,'.')
from rast import *
import json
cam=json.load(open(sys.argv[1])); out=sys.argv[2]; S=2.0
img=cv2.imread('/home/user/media/nc-configurator/photos/nc-05.jpg'); w=int(750*S);h=int(1000*S); small=cv2.resize(img,(w,h),interpolation=cv2.INTER_AREA)
V,F,C=load(); R,_=cv2.Rodrigues(np.array(cam['rvec'])); t=np.array(cam['tvec']); f=cam['f']*S
ren=render(V,F,C,R,t,f,w,h); g=cv2.Canny(cv2.cvtColor(ren,cv2.COLOR_BGR2GRAY),40,120); g=cv2.dilate(g,np.ones((2,2),np.uint8))
vis=small.copy(); vis[g>0]=(255,255,0)
kit=np.isin(C,[0x1a1a1a,0xf0c417,0xb8b8b8,0x803cee,0x4b1d96]); rk=render(V,F[kit],C[kit],R,t,f,w,h); mk=(rk!=240).any(2)
vis[mk]=(0.55*vis[mk]+0.45*np.array([0,255,255])).astype(np.uint8)
cv2.imwrite(out,vis[int(250*S):int(720*S),int(100*S):int(720*S)])
