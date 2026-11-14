#!/bin/bash
# usage: go.sh <tag> [name-in-batch]   newest download_link result in the session transcript -> batches/<tag>.tsv -> ingest
T=/home/user/Illumaesthetic-Video-Editor/projects/grimace-build-longform/tools; M=/home/user/media/grimace-build
python $T/links.py $M/batches/$1.tsv $2 && python $T/ingest.py $M $M/batches/$1.tsv 2>&1 | tail -4
