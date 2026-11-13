import json, subprocess, sys, numpy as np, librosa
sr=48000
y=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout,np.float32)
w=sr//1000; env=np.sqrt(np.convolve(y**2,np.ones(w)/w,mode="same"))
y2=librosa.resample(y,orig_sr=sr,target_sr=22050); hop=128
S=np.abs(librosa.stft(y2,n_fft=1024,hop_length=hop)); f=librosa.fft_frequencies(sr=22050,n_fft=1024)
low=S[(f>40)&(f<150)].sum(0); lo=np.diff(low,prepend=low[0]); lo[lo<0]=0
fl=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S),sr=22050,hop_length=hop)
t=np.arange(len(lo))*hop/22050
pk=librosa.util.peak_pick(lo,pre_max=10,post_max=10,pre_avg=40,post_avg=40,delta=lo.max()*0.10,wait=30)
out=[]
for p in pk:
    c=t[p]; a,b=max(0,int((c-0.06)*sr)),int((c+0.05)*sr); seg=env[a:b]; k=int(np.argmax(seg))
    base=np.percentile(seg[:max(1,k)],10); half=base+(seg[k]-base)/2; i=k
    while i>0 and seg[i]>half: i-=1
    out.append((round((a+i)/sr,4), round(float(lo[p]/lo.max()),2)))
json.dump(out,open("kicks.json","w"))
print(len(out)); print([o for o in out if o[0]<48])
