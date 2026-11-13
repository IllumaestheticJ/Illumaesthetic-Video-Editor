import subprocess, sys
from PIL import Image, ImageDraw
src,t0,t1,step,cols,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
W,H=480,270; ts=[]; t=t0
while t<t1: ts.append(t); t+=step
rows=(len(ts)+cols-1)//cols; m=Image.new('RGB',(cols*W,rows*H))
for i,t in enumerate(ts):
    p=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',src,'-frames:v','1','-vf',f'scale={W}:{H}','-f','image2pipe','-vcodec','png','-'],capture_output=True)
    import io
    try: im=Image.open(io.BytesIO(p.stdout))
    except Exception: continue
    d=ImageDraw.Draw(im); s=f'{int(t//60)}:{t%60:04.1f}'; d.rectangle((0,0,60,14),fill='black'); d.text((3,1),s,fill='yellow')
    m.paste(im,((i%cols)*W,(i//cols)*H))
m.save(out,quality=80); print(out,m.size)
