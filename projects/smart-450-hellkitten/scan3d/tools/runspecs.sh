# runspecs.sh spec.json ... : render each spec in turn (one Blender at a time), log to specs/<name>.log
for s in "$@"; do
  n=$(basename $s .json)
  (cd /tmp && /usr/local/bin/blender -b -P /home/user/Illumaesthetic-Video-Editor/projects/smart-450-hellkitten/tools/shot.py -- $s > /home/user/media/work/smart-450/scan3d/specs/$n.log 2>&1)
  echo "DONE $n $(grep -c Saved /home/user/media/work/smart-450/scan3d/specs/$n.log) frames $(date +%H:%M:%S)"
done
