#!/bin/bash
# solve_car.sh CAR : solve the three photo cameras (A,B,C) in the model frame
C=$1; D=/home/user/media/cars/$C/match; cd $D
for a in A B C; do
  [ -f cam_${a}.json ] && [ -z "$FORCE" ] && continue
  python /home/user/Illumaesthetic-Video-Editor/tools/photo1to1/solve_angle.py $a.jpg ${a}_mask.png ../scan/glb.npz cam_$a.json 2>&1 | grep -E "coarse top|SOLVED|rror" | sed "s/^/$C $a /"
done
