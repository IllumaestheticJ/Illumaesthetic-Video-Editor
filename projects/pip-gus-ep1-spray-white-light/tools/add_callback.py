"""Series v0.4 (owner 2026-11-17): prepend Gus's callback "We scan the car." as shot O (frames -45..-1) to ep1_timeline.json.
The clip (Higgsfield ElevenLabs v4 job 7e785fae, Harrison) starts at reel -1.30 s; word times from medium.en + energy onset.
    python tools/add_callback.py ep1_timeline.json /home/user/media/ep1/voice/callback_words.json"""
import json, sys
tl_p, cw_p = sys.argv[1], sys.argv[2]
tl, cw = json.load(open(tl_p)), json.load(open(cw_p))
START, F0 = -1.30, -45
tl["lines"] = [L for L in tl["lines"] if L["n"] != 0]
tl["shots"] = [s for s in tl["shots"] if s["id"] != "O"]
ws = [dict(w=w["w"], t0=round(START + w["t0"], 3), t1=round(START + w["t1"], 3)) for w in cw["words"]]
tl["lines"].insert(0, dict(n=0, speaker="GUS", text="We scan the car.", shot="O", file="callback.mp3", clip_start=START,
                           t0=ws[0]["t0"], t1=ws[-1]["t1"], seg0=START, words=ws))
tl["shots"].insert(0, dict(id="O", f0=F0, f1=0))
tl["opening_frames"] = -F0
json.dump(tl, open(tl_p, "w"), indent=1)
print("O", F0, ws)
