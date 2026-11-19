#!/bin/bash
# v1.2: box cutter (s1), continuous wing+lip (s23), plate moved into the recess (s7-9 region re-render + patch).
# Final quality: 1080x1920, 32 spp + denoise, true 60 fps. Resumable; each finished shot is saved to the Shared Drive.
cd "$(dirname "$0")"
W=/home/user/media/bf-integra-385-combo/work; R=$W/render_hq12; P=$W/render_hq12_plate; mkdir -p $R $P
REPO=/home/user/Illumaesthetic-Video-Editor
B="blender -b --factory-startup -P shots.py -- --res-pct 100 --samples 32 --step 1 --fps60 --reg-dir $W/reg3"
save() { (cd $REPO && python scripts/vdrive.py save bf-integra-385-combo $1 $2 > /dev/null 2>&1) ; }
for s in 1 23; do
  echo "$(date -u +%H:%M) start shot $s"; find $R/s$s -name '*.png' -size 0 -delete 2>/dev/null
  $B --shot $s --out $R/s$s >> $R/s$s.log 2>&1
  echo "$(date -u +%H:%M) shot $s done $(ls $R/s$s | wc -l) frames"; save frames_hq12_s$s $R/s$s
done
for s in 7 8 9; do
  echo "$(date -u +%H:%M) start plate region shot $s"; find $P/s$s -name '*.png' -size 0 -delete 2>/dev/null
  $B --shot $s --out $P/s$s --plate-border >> $P/s$s.log 2>&1
  python3 patch_plate.py $s >> $P/patch.log 2>&1
  echo "$(date -u +%H:%M) shot $s patched $(ls $R/s$s | wc -l) frames"; save frames_hq12_s$s $R/s$s
done
echo ALL_DONE
