"""Edge overlay of the configurator model (cyan edges) + kit (yellow tint) on the photo. usage: onion.py cam.json out.jpg [scale]"""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from rast import *
import json
cam=json.load(open(sys.argv[1])); out=sys.argv[2]; S=float(sys.argv[3]) if len(sys.argv)>3 else 1.5
PH='/home/user/media/de5-configurator/photos/gt_acura-integra-de5-gt-wing-rear-quarter-white.jpg'
img=cv2.imread(PH); w=int(cam['w']*S);h=int(cam['h']*S); small=cv2.resize(img,(w,h),interpolation=cv2.INTER_AREA)
V,F,C=load(); R,_=cv2.Rodrigues(np.array(cam['rvec'])); t=np.array(cam['tvec']); f=cam['f']*S
ren=render(V,F,C,R,t,f,w,h); g=cv2.Canny(cv2.cvtColor(ren,cv2.COLOR_BGR2GRAY),40,120); g=cv2.dilate(g,np.ones((2,2),np.uint8))
vis=small.copy(); vis[g>0]=(255,255,0)
kit=np.isin(C,[0x1a1a1a,0xf0c417,0xb8b8b8,0x803cee,0x4b1d96]); rk=render(V,F[kit],C[kit],R,t,f,w,h); mk=(rk!=240).any(2)
vis[mk]=(0.6*vis[mk]+0.4*np.array([0,255,255])).astype(np.uint8)
cv2.imwrite(out,vis)
