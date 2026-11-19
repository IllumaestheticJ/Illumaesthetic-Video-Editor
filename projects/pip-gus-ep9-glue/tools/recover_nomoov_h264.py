# Usage: python recover_nomoov_h264.py BROKEN.MP4 OUT.h264 REF_SPS_PPS.h264   (REF: ffmpeg -i GOOD.MP4 -map 0:v -c copy -bsf:v h264_mp4toannexb -frames:v 1 -f h264 ref.h264)
# then: ffmpeg -r 24000/1001 -i OUT.h264 -c copy rec.mp4  (rotate with -noautorotate + transpose=1 to match the DJI portrait clips)
"""Recover an H.264 elementary stream from a DJI MP4 whose moov is missing: walk the mdat as 4-byte length-prefixed NALs;
when a length/header is implausible (an interleaved AAC or metadata chunk), scan forward for the next plausible NAL pair."""
import sys, struct
src, out, ref = sys.argv[1:4]
d = open(src, 'rb').read()
o = open(out, 'wb')
o.write(open(ref, 'rb').read().split(b'\x00\x00\x00\x01\x65')[0])   # SPS/PPS (and SEI) from the reference file
def ok(p):
    if p + 5 > len(d): return False
    L = struct.unpack('>I', d[p:p + 4])[0]
    if L < 2 or L > 8_000_000 or p + 4 + L > len(d): return False
    h = d[p + 4]
    return (h & 0x80) == 0 and (h & 31) in (1, 5, 6, 7, 8, 9) and ((h >> 5) & 3 or (h & 31) in (6, 9))
p, n, skips, frames = 44, 0, 0, 0
while p + 8 < len(d):
    if ok(p):
        L = struct.unpack('>I', d[p:p + 4])[0]
        q = p + 4 + L
        if q + 5 > len(d) or ok(q) or True:
            t = d[p + 4] & 31
            if t in (1, 5): frames += 1
            o.write(b'\x00\x00\x00\x01' + d[p + 4:q]); p = q; n += 1
            continue
    # resync: find next p' where two consecutive plausible NALs start
    p2 = p + 1
    while p2 + 8 < len(d):
        if ok(p2):
            L = struct.unpack('>I', d[p2:p2 + 4])[0]
            if ok(p2 + 4 + L) or p2 + 4 + L >= len(d) - 8:
                break
        p2 += 1
    skips += 1; p = p2
print("nals", n, "frames", frames, "resyncs", skips)
