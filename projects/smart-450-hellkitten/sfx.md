# Meow sound sources (v3)

All files are in `/home/user/media/work/smart-450/sfx/src/` (never executed; decoded only by ffmpeg). Fetched 2026-11-13 with a generic `curl` user agent; nothing about the owner or project was sent.
Only CC0 / public-domain recordings were taken (no NC, ND or share-alike).

| file in sfx/src | page / URL | author | licence | fetched | used for |
|---|---|---|---|---|---|
| JorgeTheCatMeowing__Untitled3.ogg | https://archive.org/details/JorgeTheCatMeowing (file Untitled3.ogg, 53 s) | uploader not named on the item ("Jorge the cat meows... alot") | CC0 1.0, http://creativecommons.org/publicdomain/zero/1.0/ (item metadata `licenseurl`) | 2026-11-13 | tiny_a, short_b, short_c, mid_d, long_h, long_i, chirp_j (7 of the 10 one-shots) |
| meow_20220616__meow_.wav | https://archive.org/details/meow_20220616 (file meow!.wav, 3.3 s, item dated 2015-06-09) | uploader "meow" | CC0 1.0, same URL as above (item metadata) | 2026-11-13 | big_f, big_g |
| wm__2015-11-24_Niaou_Tsester.flac | https://commons.wikimedia.org/wiki/File:2015-11-24.νιαούρισμα.Νιάου.noise_reduced.flac (upload.wikimedia.org, 1.2 s) | Tsester (Wikimedia Commons) | CC0 (Commons licence field) | 2026-11-13 | sad_e |

Not used: six more CC0 / public-domain Commons meows were identified (Maullido de gata hembra, M. de gata hembra joven, Meow of a Siamese cat - freemaster2, Black cat sound begging the foods, Meow of a pleading cat, GettingOutImpatient) but upload.wikimedia.org rate-limited this machine (HTTP 429 for 15 minutes) so they were not fetched. An archive.org field recording of a cat (aporee_47968_54535, public-domain mark) was found but not used (door scratching, noise).
Licence checks: Commons licence from the API `extmetadata.LicenseShortName`; archive.org from the item's `licenseurl` field. These are the uploaders' statements; nobody verified the recordings' provenance further.

## One-shots (sfx/oneshots/, built by tools/meows.py)
Segment cut at the listed start, 4th-order high-pass 250 Hz, onset = first 2 ms-RMS sample above 20 % of the segment peak, trimmed to 3 ms before it, 50 ms tail fade, peak-normalised, then pitch-shifted by resampling (pitch and length together) toward the nearest tone of A minor (the track's key: bass chroma A 27 %, key profile A minor 0.64 / A major 0.59). Shifts are +0..+5.5 semitones (one -2.25), so they stay cat-like. They are adult-cat recordings pitched up, not kittens: no CC0 kitten recording was found in the time available.
Per-one-shot source segment, estimated f0 and applied shift: `meow_map.json`.
