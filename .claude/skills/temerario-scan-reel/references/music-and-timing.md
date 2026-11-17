# Music, beat grid and cut timing

## Choosing the track

1. Use the track the user supplied. Otherwise pick from Dropbox `/Moosic`, or a real track the user named. Never use a
   generated or library track (MR2 SW20, QX80, Civic).
2. Check that no other reel already uses it: grep `projects/*/project.yaml` and the `editlog.jsonl` files for the title and
   `song_clip_id`.
3. Start from the song's beginning unless the user gives an offset. Then confirm the drop lands where the edit needs it.
   Megalomaniac's kick entry at 15.52 s and drop at 45.515 s are exactly 64 beats apart at 128.05 BPM.
4. YouTube is blocked from cloud sessions, and getting past its bot check is not allowed. Ask the user to upload the audio.

## Finding the grid (one method is not enough)

- **`ive beats` can report half or double the tempo** (GR86: 61.5 vs a real 122 BPM; GD trio: 161 vs 122).
- **Four-on-the-floor:** take the 40-120 Hz envelope peaks. The kick attack is about 45 ms before the low-pass peak.
  A broadband half-rise check locks onto the off-beat bass and reads every cut half a beat late (GT3 RS v5).
- **Syncopated house:** get the bar from low-band flux autocorrelation at 2- and 4-bar lags. Print a quarter-beat accent
  table from the drop, and cut on measured kick attacks (GD trio v2).
- **Bass in the kick band:** a spectral-flux grid fit over the excerpt (librosa onset_strength, median aggregate) gave the
  true tempo (GR86 v5).
- **Live or funk feel:** don't fit a grid. Measure each strong low-band hit individually
  (`projects/suzuki-cappuccino/tools/onsets2.py`), then pick the start offset that rounds all cuts to within half a frame.
- **Drumless breaks:** cut on phrase hits (the Civic scan-process v5 was approved this way).

## Laying cuts

- Every shot is a whole number of bars, or one bar per shot on fast reels. GR86 v4 cuts on every kick, about 2.45 s apart,
  with one 0.4-1.0 s action per shot.
- Keep cameras and keys in bars in the shot list, so a re-time is one edit. A music swap on the same grid reuses every render:
  src_fps = 15 x planned frames / new frames.
- Hard cuts only for state swaps. A splice inside the music goes on a downbeat with a ~20 ms crossfade.

## Verifying

- Measure cut offsets on the DECODED audio of the delivered mp4, to within ±½ frame. The dip window must straddle the cut
  (g-30 to g+5 ms); a window that ends 40 ms early reports every cut about 45 ms late (GR86 v4).
- When two hits are less than 150 ms apart, the half-rise onset can latch onto the wrong one. Confirm with the envelope's
  rise rate.
- Loudness: about **-14 LUFS integrated, true peak below -1 dBFS**, measured with ebur128 AFTER the mux, because AAC adds
  peak. Turn the music down, never up. If the ceiling and the target disagree, the ceiling wins.
- `scripts/verify_delivery.py out.mp4 --cuts ... --lock <frame>` runs the delivery checks.
