# Character design (locked 2026-11-14, owner: "dot eyes, they're now cute")

Homage in *build* to Krinkels' Thing-Thing / Madness Combat (owner's references), made
family-friendly and in 3D. Own outfits only - no bandage face / red round goggles.

## Shared build (every character)
- Light-grey egg-shaped head on a light-grey rounded pill/capsule body, matte vinyl-toy material.
- **NO ARMS, NO SHOULDERS.** Clothing is a straight tube (no sleeves, sleeve stubs or shoulder bulges). Two rounded mitten hands float clearly detached (about 0.8 hand-width gap since v7).
- Two dark-grey stubby rounded feet, no legs.
- **Face: two small black dot eyes, nothing else** (no crosshair, no mouth). Owner removed the crosshair.
- Palette: greyscale + sage green #619f73 only (brand accent). No text/logos on clothes.

## Gus (dad, voice Bob)
Tallest of the two (~1.5 m to the top of the head since v7). Welding goggles with sage lenses pushed up on head; sleeveless charcoal work vest with pockets.

## Pip (kid, voice Kiki)
Noticeably smaller than Gus (~1.1 m, about 70 % of his height since v7). Backwards dark-grey cap; sleeveless oversized sage hoodie, white drawstrings;
small handheld 3D scanner.

## Extras (from the lineup, optional)
Scan tech (headset + lens monocle), painter (splattered apron, brush), shop owner (mustache, sage bandana),
driver (open-face helmet with sage stripe).

## Higgsfield reference job ids (gpt_image_2_6, low/1k)
- lineup, blank faces: 2094da79-99eb-47b4-b533-477a066b8a27
- dad+kid in shop, dot eyes: a1f2e424-8bf9-40c4-860f-d0c6809f5cdd
- dad face options (B = pick): c9ddd31c-620e-4308-824e-2b8bf9a25929
- kid face options (B = pick): 315f3988-568a-4217-b33c-8850455cff6e
- dad turnaround (FINAL): 31001f1d-965b-4949-97d9-b10e40e10e7a
- kid turnaround (FINAL, no arms): 9cbf5fb5-0492-4c75-a771-a67ba61f647c  (3c6d49df... rejected: hoodie shoulders read as arms)
Use these as image_references for any new shot to keep the characters consistent.
Note: Higgsfield unlimited is not available from Claude Code; keep to gpt_image_2_6 low/1k (~0.5 cr/image).

## Shading (owner, 2026-11-14): CEL-SHADED world
Whole cartoon world is cel-shaded (EEVEE toon: 2-3 hard bands, black outlines, thicker on characters).
Real IS350 footage in the phone stays photographic (cartoon -> real -> scan contrast).
Reference: cel_ref e749a062-b917-4ba6-b13b-82e02acd7626 (ignore its vest arm-hole circles and hand touching head).


## Expressions (owner pick 2026-11-16: option B)
No eyebrows. Floating brows read as a second pair of eyes. Expressions come only from the eye shape: round dot (neutral), flat D-cut tilted inner-down (annoyed), half-moon tilted inner-up (worried), lines (squeezed), ^ ^ arcs (excited), 1.3x round pop (surprised).

## Name badges (owner, 2026-11-16)
Both wear a small Illumaesthetic name badge, pinned (no arms) on the chest at the wearer's left (screen right when facing camera):
- Flat rounded rectangle, near-white #ecefec with the cel outline, thin sage #619f73 top stripe; the Illumaesthetic logo
  (remotion/public/illumaesthetic_logo.png, the end-card logo, as is) on top and the name below in black Fjalla One (GUS / PIP).
- About 1/4 of the torso width: Gus 11 cm, between his chest-pocket flap and the collar; Pip 8.5 cm, beside his drawstrings,
  tilted ~4 deg. It lies flat on the clothing tube and squashes/stretches with the torso.
- Readability: the name just reads in medium shots and clearly in close-ups; the logo is a smudge at phone size (accepted).
- Built by `nametag()` in tools/partA_scene.py from textures made by tools/nametag_tex.py.

## Faces: no brows (owner pick, 2026-11-16)
Brows were removed (they read as a second pair of eyes). Expressions come from the dot shape alone: round (neutral), flat cut
tilted inner-down (annoyed / weary), cut tilted inner-up (worried / frustrated), lines (squeezed), ^ ^ arcs (excited), 1.15x
(curious), 1.3x pop (surprised); one D-cut + one round = skeptical; tilted cuts take at least 40 % of the dot and the shaped
eyes scale 1.1x so they read at phone size.

## Proportions (owner pick 2026-11-16: concept row 3, from v7 on)
Halfway between "a little closer" and the Madness-grunt look (preview/proportion_concepts.jpg, row 3):
- Rounder head (height -6 %, width +6 % vs v6), egg taper -0.091 (was -0.13); eyes sit a little lower on the face.
- Short torso: about 1.1 head-heights from hips to neck (Gus neck 0.80 m, was 1.13 m; Pip 0.52 m, was 0.61 m).
- Body 15 % wider, hips 1.5x higher, feet 18 % bigger, hands slightly closer to the body (gap x0.78).
- Hands, eyes, clothes, nametags, palette unchanged. Canonical numbers: GUS_SPEC / PIP_SPEC in tools/partA_scene.py.
