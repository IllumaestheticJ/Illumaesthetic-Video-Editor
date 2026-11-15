# Ferrari 296 GTB scan reel v8 - self-review (v7: review_v7.md)

User on v7: "available now is too low on the scan" / "im pretty certain there were underhood plastics that weren't
included (check for me)" / "start with the car being red (cause ferrari)" / "im also certain there were more parts removed
than this".

Check: the Drive folder has 28 scans; 6 had never been fetched. Two ("Frunk Trim", "Frunk Trim ") are the plastics the
user remembered - they register onto the ENGINE BAY (rear; mid-engine): left + right side trims and a cross panel behind
the cabin. The other 4 are second captures of parts already shown (rear bumper inner without diffuser, front end removed,
sill with skirt off, side skirt). Fender Bracket (25k tris) still unused.

v8 = v7 timing (cuts 124, 298, 347, 446, 521, 732, 956) with:
- 13 moving parts (v7: 9): + glass engine lid (split from the car scan: its surface is absent from the lid-off Engine Bay
  scan; lifts with the louvred cover k42-44) + 3 engine-bay trims (cut out of the composite within 7 mm, lift out of the
  open bay k51-53, splay outward; in the blast). New label ENGINE BAY TRIM / LEFT · RIGHT · CROSS PANEL (662-706).
- Body Ferrari red; every part starts red (opening car fully red) and turns its own colour over 0.3 s when it first
  leaves home. Rear bumper -> pearl, exhaust -> green, trims lime. Red needed matte body + AgX Punchy + exposure -1.7.
- CTA "SCAN DATA AVAILABLE NOW" + URL pill moved from the bottom edge up onto the empty lower part of the gallery photo.

Output: `/home/user/media/work/f296/out/ferrari_296_v8.mp4` - 1080x1920, 30 fps, 38.00 s, h264 + AAC.
Checked: trims + lid registration stills (home / lifted, no copy left behind), 4 red tests, test frames before the full
render, every render (counts, 0 dark), contact sheets of all 7 shots, frames at the new label and at the 1:1 cut (955/956),
CTA still, probe, `ive director` (one flag: s1_wide "dead frames" - metric artifact of the darker red, motion = v7).

Scores as v7 except: Story 4 -> 5 (engine bay now opened down to the trims; 13 parts). Grade 4 (red body reads Ferrari;
whole frame darker at exposure -1.7 - wheels/tyres are body red too). Scan quality 3: the bay under the trims shows
small dark gaps where the trims were cut.
Open: Fender Bracket unused; tyres red (one body mesh).

---
# Ferrari 296 GTB scan reel v7 - self-review (v6: review_v6.md)

User on v6: "when scrolling through the different photos/options, change the dropdown so the scan price reflects the
photo, and then re-render with all scans in a different color" -> chose "Each part its own color". Then: "dont change the
dropdown in the actual product, change the dropdown in the video" (nothing on the store was ever changed: the options were
picked in a local headless browser like a visitor and screenshotted).

v7 = v6 timing (cuts 124, 298, 347, 446, 521, 732, 956) with:
- every scan shot re-rendered with a palette: body green, hood yellow, front bumper pink, wheel blue, fender amber, skirt
  teal, rear bumper salmon, diffuser violet, engine cover sky, exhaust orange (satin BSDF, tools/palette.py).
- CTA: each carousel swipe (k80-k85) lands on the photo the site itself shows for a Dataset option (variant featured
  image), and the page under it switches to that option's screenshot, so the dropdown + price match the photo:
  Front Bumper $1,000, Hood $800, Rear Bumper $1,000, Engine Bay $600, Side Skirt $800, Fender $800; All Data $4,000 with
  the CTA (k86). Green outline pulses on the dropdown + price at each change. Prices are the site's, nothing typed.

Output: `/home/user/media/work/f296/out/ferrari_296_v7.mp4` - 1080x1920, 30 fps, 38.00 s, h264 + AAC.
Checked: every color render (frame counts, 0 dark), contact sheets of all 7 shots, HUD labels over the colored scans,
frames 954-956 at the 1:1 cut, CTA stills per option, probe, `ive director` (only flag: 0.8 s still at the very end =
URL hold, kept).

Scores as v6 except: Grade 5 -> 4 (deliberate departure from the house silver look at the user's request; the parts now
read apart instantly, but the 1:1 cut now also changes colour, colored scan -> grey website render). Text 5: dropdown and
price follow each photo from the site's own variant data.
Open: salmon rear bumper and amber fender are close-ish hues (never in frame together except the drop).

---
# Ferrari 296 GTB scan reel v6 - self-review (v5: review_v5.md)

User on v5: "add the mobile version CTA for the scan data at the end with the 1:1 transition of the website photos".

v6 = v5 up to the lock (k71), then a new ending (replaces the fade + logo card):
- k71 -> k75: the locked car swings round the nose onto the camera solved against the listing's cover photo (the
  website photos are grey renders of this same scan); k75 = hard 1:1 cut from the silver scan to that photo.
- the photo is in the phone layout of illumaesthetic.com/products/ferrari-296-gtb-type-f171-3d-scan-2022 (Playwright,
  iPhone 14 Pro, 393x699 = 9:16); zoom out k75 -> k79 into its gallery slot, carousel swipes land on k80/k82/k84
  (front bumper explode, rear 3/4, rear bumper + engine explode - the listing's own photos), "SCAN DATA / AVAILABLE NOW"
  k85, "ILLUMAESTHETIC.COM" k86, slow push-in to the end (Remotion MobileCTA, cta.json).

Output: `/home/user/media/work/f296/out/ferrari_296_v6.mp4` - 1080x1920, 30 fps, 38.00 s, cuts unchanged (956 = k75).
Checked: cover-photo camera by edge overlay (wheels, headlights, windscreen, mirror, side intake on the photo's);
frames 955/956 overlaid at the cut; near-duplicate/dark scan (only the 6-frame hold on the 1:1 frame + the arrival);
`ive director` (no flags); every CTA phase in a contact sheet.

Ending score 5 -> 5 (now a CTA that lands on the product). Text 4: CTA wording is the listing's ("scan data ... is now
available"), no numbers added; the page's own price shows faintly above the CTA.
Open: the scan composite and the website scan differ slightly at the front lip and sill (both visible across the cut
by ~10-20 px); the site may change - the page was captured 2026-11-12.

---
# Ferrari 296 GTB scan reel v5 - self-review (v4: review_v4.md)

User on v4: "re-edit it to this song (Buckshot Roulette OST - General Release), learn from the GT3RS video editor on what
to change. right now, not enough of the parts are blown up or shown."

v5: 9 moving parts (v4: 7) - hood, front bumper, + FRONT WHEEL (arch filled from the wheel-off "Brake Disk" state scan:
disc, caliper, hub, liner), fender, side skirt, rear bumper, diffuser, engine cover, + EXHAUST TIP. GT3RS pattern:
every part comes off on a kick where the camera is and STAYS off (progressive explode), one label per part, then all 9
blast out together on the drop (k57), drift, fly home k69 and lock k71, fade, logo (660 px).

Output: `/home/user/media/work/f296/out/ferrari_296_v5.mp4` - 1080x1920, 30 fps, h264 yuv420p + AAC, 38.00 s (1140 frames).
Cut frames 124, 298, 347, 446, 521, 732, 956.

Checked: max luma of every render frame (0 bad); first/quarter/middle/three-quarter/last sheets of the new shots;
frames at every label window before placing labels and again composited (labels type on, all complete); per-frame
near-duplicate + dark scan of the final mp4 (0 / 0 before the fade); cuts vs measured kicks; `ive director`; probe.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car turning from frame 1 over the intro bars. |
| 2 | Beat sync | 5 | Kicks measured on the decoded 40-120 Hz band; every cut within +-16 ms (half a frame) of a kick; drop cut on k57. Part motions start on kicks (wheel k27, fender k30, skirt k35, rear bumper k37, diffuser k38, cover k42, exhaust k46, blast k57, lock k71). |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 3 | Composite interiors ragged where state scans overlap; rear bumper inner face speckled; wheel bottom 31 mm completed by rotating the wheel 144 deg (5 double spokes, spoke-for-spoke). |
| 5 | Story | 4 | front -> wheel -> side -> rear -> everything off from above -> drop blast -> lock. Parts stay off, so by the breakdown the car is visibly stripped. |
| 6 | Grade | 5 | One AgX silver look across old and new shots. |
| 7 | Text | 4 | 9 labels, one per part, scan shots only, wording from scan files, no numbers. Short windows on the side shot (30-32 frames) because the parts come off fast on consecutive kicks. |
| 8 | Ending | 5 | Lock on k71, fade, logo in on k77 with the track fade. |
| 9 | Technical | 5 | Spec correct; 0 duplicated/black frames before the fade. |

## Open points
- `ive director`: s1_wide ~ v5_drop (IoU 0.71) - bookend whole-car view, kept. v5_drop "dead frames 1.7 s" = the locked
  car holding before the fade, kept.
- The drop opens with the front bumper partly leaving frame bottom-right.

## For the next agent
- Wheel axle: least-squares intersection of tread-triangle normals, not a hub-face circle fit (that was 100 mm off).
- shot.py: aiming the camera target LOWER moves the subject UP in frame.
- Don't retime interpolated renders with `speed:` (drops 1 frame in 19 -> judder); change `src_fps` instead.
