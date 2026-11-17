#!/bin/bash
# render the given shots one at a time (heavy jobs serialised)
cd "$(dirname "$0")/.."
for s in "$@"; do
  blender -b --factory-startup -P tools/shot.py -- specs/$s.json > /home/user/media/bf-miata-mr2-night-meet/work/$s.log 2>&1
  echo "$s $(ls /home/user/media/bf-miata-mr2-night-meet/work/$s/*.png 2>/dev/null | wc -l) frames" >> /home/user/media/bf-miata-mr2-night-meet/work/queue.log
done
echo QUEUE_DONE "$@" >> /home/user/media/bf-miata-mr2-night-meet/work/queue.log
