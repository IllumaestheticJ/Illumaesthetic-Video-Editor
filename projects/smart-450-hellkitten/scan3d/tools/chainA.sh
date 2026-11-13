S=/home/user/media/work/smart-450/scan3d/specs
for n in a1_match_str a2_body_on_off a3_detail; do
  bash /home/user/media/work/smart-450/scan3d/tools/runspecs.sh $S/${n}_final.json
  python3 /home/user/media/work/smart-450/scan3d/tools/finalize.py /home/user/media/work/smart-450/renders/$n 15 30 1080x1920
done
echo CHAIN_A_DONE
