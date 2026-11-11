#!/bin/bash
# Fetch each Revuelto scan from Drive, decimate to 2 mm (out of core), delete the raw STL to save disk.
#   tools/fetch_queue.sh <list.tsv>   (lines: drive_id<TAB>short_name)
set -u
RAW=/home/user/media/lamborghini-revuelto/scans
DEC=/home/user/media/lamborghini-revuelto/dec2
mkdir -p "$RAW" "$DEC"
cd /home/user/Illumaesthetic-Video-Editor
while IFS=$'\t' read -r id name; do
  [ -z "$id" ] && continue
  [ -f "$DEC/$name.stl" ] && { echo "skip $name"; continue; }
  src=$(python -c "import sys; from ive.fetch import drive_download; print(drive_download(sys.argv[1], sys.argv[2]))" "$id" "$RAW" | tail -1)
  echo "fetched $name -> $src"
  python -m ive decimate "$src" "$DEC/$name.stl" --cell 2 && rm -f "$src"
  echo "done $name"
done < "$1"
echo QUEUE_DONE
