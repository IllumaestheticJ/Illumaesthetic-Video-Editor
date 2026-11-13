import subprocess, numpy as np, sys, json
from scipy.signal import butter, sosfiltfilt
SR=44100
def dec(f):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True,check=True).stdout,np.float32).astype(np.float64)
def segs(x, thr_db=-30, min_gap=0.12, min_dur=0.12):
    hp=sosfiltfilt(butter(4,300,'high',fs=SR,output='sos'),x)
    w=int(0.01*SR); env=np.sqrt(np.convolve(hp**2,np.ones(w)/w,'same'))
    pk=env.max(); on=env>pk*10**(thr_db/20)
    out=[];i=0;n=len(on)
    while i<n:
        if on[i]:
            j=i
            while j<n and (on[j] or (j<n and on[j:j+int(min_gap*SR)].any())): j+=1
            if (j-i)/SR>=min_dur: out.append((i/SR,j/SR))
            i=j
        else: i+=1
    return out,env,hp
def f0(x):
    seg=x[:int(0.08*SR)]
    if len(seg)<2000: return 0
    ac=np.correlate(seg,seg,'full')[len(seg)-1:]
    lo,hi=int(SR/1500),int(SR/200)
    k=lo+np.argmax(ac[lo:hi]); return SR/k
if __name__=='__main__':
    for f in sys.argv[1:]:
        x=dec(f); s,env,hp=segs(x,thr_db=float(-26))
        print(f,len(x)/SR,'s',len(s),'segments')
        for a,b in s[:40]:
            i=int(a*SR); mid=x[int((a+b)/2*SR):int((a+b)/2*SR)+3000]
            print('  %.2f-%.2f dur %.2f peak %.1fdB f0~%.0f'%(a,b,b-a,20*np.log10(np.abs(x[int(a*SR):int(b*SR)]).max()+1e-9),f0(mid)))
