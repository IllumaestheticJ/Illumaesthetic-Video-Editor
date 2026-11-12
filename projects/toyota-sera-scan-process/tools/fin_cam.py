import json,math,subprocess,sys,numpy as np
W='/home/user/media/work/sera'
a,d,h,foc,tx,tz=[float(x) for x in sys.argv[1:7]]; out=sys.argv[7]
f=np.array([0.258,0.966]); l=np.array([-0.966,0.258]); ar=math.radians(a)
v=f*math.cos(ar)+l*math.sin(ar); loc=v*d
subprocess.run(['python','-m','ive','lookat',out,f'--loc={loc[0]:.3f},{loc[1]:.3f},{h}',f'--target={tx*f[0]:.3f},{tx*f[1]:.3f},{tz}','--focal',str(foc),'--sensor','14.175','--size','1080x1920'],check=True,capture_output=True)
c=json.load(open(out)); c['shift_x']=-0.0291+float(sys.argv[8]) if len(sys.argv)>8 else -0.0291; c['shift_y']=-0.381+(float(sys.argv[9]) if len(sys.argv)>9 else 0); json.dump(c,open(out,'w'),indent=1)
