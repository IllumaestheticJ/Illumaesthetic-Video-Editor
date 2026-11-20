# gta6-integra: self-review

## v1 draft (2026-11-20) - no owner review yet
Output: `/home/user/media/work/out/gta6-integra_v1.mp4`, 1080x1920, 30 fps, 28.2 s (847 menu frames, no end card, no radio).
Brief: "the exact same thing as the Civic reel (gta6-customs v19), for the Integra kit including the widebody", arriving as a
session brief rather than from the owner in chat; all nineteen Civic rounds applied from the start.

Structure as built: stock car in Apex Blue > Front Lip (front camera) > Fender Flares (new high rear three-quarter camera) >
Side Skirts (low front quarter) > Rear Spats (new low rear quarter camera) > Trunk Lip and Rear Wing (rear camera), each entered
from the list and left back to it with the row marked > Cosmetics / Respray, Recommended tab, ten factory colours, ends on the
lookbook grey > Performance / Suspension (game's kit, $750) > Wheels / Rim Style (bronze 6-spoke, $560) > frozen UI-free shop
frame with the line once. Wallet $4,220 to $0.

Missing, and why:
- **End card**: the wordmark is in the Epsilon-Site repo (attach refused in this session) and the palm-sunset background was
  not in the Dropbox folder. No substitute drawn (Civic v17-v19). `assemble4.py` adds the card when both files exist.
- **Honey FM bed**: `radio.wav` not in the Dropbox folder. The Civic's bed was 26.8 s of music; this shop section is 28.2 s.
- **Site GLB v8 / catalogue file / lookbook notes**: same repo. Model from the Drive bundle (v29 export), prices from the store.

Checked by looking (delivery size): all nine purchase frames (part visible and in frame, background beside the car, pop-up,
wallet figure); one frame from each of the sixteen whips (only lettering and the stats panel sharp); every menu state on a
sheet; first and last colour side by side. Fixed on the way: game car visible through the Integra's glass; mirrored menu
lettering in the fills; panorama mirrored as yellow and green blocks in the rear glass; spats hidden under the option block
(camera moved); respray counter drawn with its box; white-to-grey respray too weak (entrance colour changed to blue).
Checked by measurement, not by ear: purchases -25.4 dB, room tone -43 dB, speech band 0.95 s after each purchase back at room
tone (-54 dB, was the Civic's test for the hidden voice), left = right during the chime, the line once at 26.4 s (-26 dB).
Frame count 847 = timeline; h264 yuv420p, AAC 48 kHz, faststart.

Weak, known:
- Trunk Lip: the model's stock car already has a small lip there; the before/after difference is slight.
- Trunk Lip and Rear Wing share the rear camera back to back.
- Side Skirts, suspension: the low front-quarter view crops the nose; a soft filled patch above the stats panel.
- Respray counter and block sit over the car's nose (grey digits on a light car are faint).
- Fender Flares screen is a frozen frame (a mechanic stands behind); the game's "Leave when ready" shows faintly through the shadow.
- The model's stock wheels are already a dark 6-spoke, so the wheel purchase reads mainly as a colour change.
- Part screens are 1.67 s each: short for reading a price.
- Acura badges on the car under a Dinka tag. Stat bars are the game's for its own car.

Self-score (rubric; beat sync and 1:1 match do not apply to this format): hook 4, story 4, text 4 (true prices; two inferred
names declared), ending 1 (no card), technical 4.

Process notes for the next agent:
- I rendered twenty stills before comparing the first and last respray colours in the shop light. Compare them first.
- Two cameras had to be re-fitted for this car although the body sizes match: a part can still land under the menu.
- A background wait with a short time limit killed a 7-minute composite; give long composites their own long timeout.

## v2 (2026-11-20) - end card
Output: `/home/user/media/work/out/gta6-integra_v2.mp4`, 30.7 s. The owner's palm-sunset background and the white wordmark arrived
through the owner's Drive folder (relayed by the Civic reel's session, sha256 checked); card as Civic v19, up from black over 7
frames. Shop section identical to v1. Checked: last shop frame, card at +3 frames and full; the line still ends before the cut
(speech band -26 dB over 26.4-27.9 s), audio fades with the card. Ending score now 4. Still no radio bed (clip not received).
Open for the owner: the shop section is 28.2 s, the clip has 26.8 s of music: shorten the shop section, or let the bed fade into
the mechanic's line.
