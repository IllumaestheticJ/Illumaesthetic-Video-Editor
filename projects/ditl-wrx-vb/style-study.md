# ditl-wrx-vb: style study of the owner's 3 reference clips (2026-11-17)

Clips (local only, `/home/user/media/ditl-wrx-vb/ref/`): ref1 "noah simulator" 24.2 s, ref2 "bad day simulator"
17.2 s, ref3 "your friend who loves hypotheticals" 29.2 s. Studied from full-size frames, 5-frames-per-second strips,
frame-difference motion and audio measurements. **I can't hear audio**, and the only speech-to-text that installs
here (pocketsphinx) is too rough to give real words, so the voice section is measurements plus what the picture shows.
Their titles, characters and "skullmug" watermark are not copied.

## Art style (what to build in Blender)
1. **Frame:** 1:1 game picture, 1080x1080 at y = 420-1499 of 1080x1920; white title text in the black band above
   (two lines when long); black below.
2. **Characters: extremely low-poly, flat-shaded.** Box torsos, wedge arms, mitten hands with no fingers, a
   faceted block head. Skin and clothes are **single flat colours** with hard facet shading. Clothing detail is
   one decal (a T-shirt print). Hair is one blocky chunk (a bun, a flat-top, a wedge).
3. **Faces: 2D hand-drawn cartoon decals** on the flat front of the head: black ink outlines, huge round eyes
   with small pupils, big mouths with teeth. Expressions are whole-face swaps: manic grin, squeezed-shut eyes,
   worry lines, clenched teeth, tiny pupils. A new face about every 0.2-0.5 s while a character talks or reacts,
   and the head tilts, turns or lunges with each swap.
4. **Bodies act big:** shrugs, arms thrown wide, leaning into the lens, doubling over. Poses snap; they aren't
   smooth. Reaction scenes end on a **slow push-in to an extreme face close-up** held for 3-6 s.
5. **POV hands are real photographed hands** (cut-outs of a real arm, a real TV remote, a real power tool), not 3D
   models, posterized to match. They poke, wave, flap and jab at things; they're always in frame and always moving.
6. **Screens show real content:** real phone screenshots, a real TV home page, a real photo. So our cart, the Affirm
   step and the Accessport should look like real screen captures, not stylised UI.
7. **Environments:** simple boxes with **photo textures** (brick, carpet, wood grain, a rug, a chalkboard menu),
   warm baked-looking lamps, repeated props (a row of identical houses, a table of identical bottles).
8. **Finish:** visible **colour banding / posterization and over-sharpening** on everything (sky and walls show
   bands), low resolution, slight wobble. (This corrects my earlier note: the crunch is strong; it sits on top of
   photo textures rather than flat colours.)
9. **Camera:** handheld first-person; restless in action scenes, almost still in face close-ups (measured frame
   difference about 7-19 in action, 1-3 in the close-ups). Hard cuts every 2-4 s outside the long reaction holds.

## Voice and sound (measured)
- **Wall-to-wall and loud:** all three sit at a constant -14 to -15 dB for the whole clip. There is no silence
  anywhere; a music bed or room noise fills every gap.
- **Fast:** 3.6-4.4 sound onsets per second in ref1 and ref2 (ours: 2.3). Lines overlap the action with no pauses
  between speakers. Ref3 is slower (2.2) with a mid-clip stretch that looks like laughing (face frames + rough
  transcript "ha ha ha").
- **Big pitch swings:** roughly 19-24 semitones between low and high, i.e. shouted, squeaked and mumbled delivery,
  not a level read. (Music is mixed in, so these numbers are approximate.)
- **Raw, not studio:** the picture shows a talker who laughs, rambles and gestures. It reads as a real person
  improvising into a cheap mic, not clean text-to-speech.

## What this means for our take 1
- Take 1 is the opposite: clean, slow (2.3 onsets/s), with silences, and HIM has no emotion control.
- **Cody measures high-pitched on Seed Audio** (about 270-340 Hz on most of his lines; an adult male voice is
  usually 85-180 Hz). It may sound like a kid. Needs the owner's ear.
- To match the references: a different HIM voice that works on Eleven v4 (tags for shouting, laughing, whispering),
  faster overlapping lines, light distortion/"cheap mic" treatment, and no silences (room tone + SFX under scenes 5-6).
  Or the owner records HIM on a phone, which is the closest to the reference's sound.

## Changes to our plan
- Hands: photographed cut-out hands (owner films their own hands on a plain background, or licensed stock), not
  rigged 3D arms. Medium-brown skin per the owner; dog tags as a photographed prop or a 3D prop.
- Characters: flat-colour block bodies + ink-drawn face decals (sheets of 6-8 faces each, not 2-3).
- Screens: build the cart/Affirm/Accessport as realistic screen captures.
- Each talking beat: face swap every 0.2-0.5 s + head move; each scene ends on a push-in to a horror face.
