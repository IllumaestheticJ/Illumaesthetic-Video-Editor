# Black Friday: Epsilon mascot + confirmed BF prices (2026-11-17)

## The owner's decision: use the Epsilon mascot, Del & Eps (not Pip & Gus)

Source: the owner's concept pages, as claude.ai artifacts:
- v0.1: https://claude.ai/artifact/MyfYpve1ho7AhiTSzvRCFf
- v0.2 colour variants: https://claude.ai/artifact/E2AUcUQJsG5a937FCorTQD

Both are concept drawings only (rough SVG sketches). There is no turnaround sheet, model or rig yet.

### Who they are
- **Del (δ), the dad.** Fabricator, fit-and-finish, 1.85 m.
  - Calm, dry, a little stubborn. Short sentences.
  - He explains *why*. He never hypes a part, quotes a number he can't back up, or rushes an install.
  - Look:
    - flat cap shaped like a GT wing profile, with an endplate at the brim;
    - safety goggles on the cap;
    - a full moustache, so no lip-sync is needed;
    - a vest, and shoulders as flat and wide as a splitter.
  - Props: calipers, straightedge, masking tape (his colour is tape-yellow), drill template, a marker behind his ear.
  - Lines: "Measure twice, drill once." "The scan doesn't lie. People do." "Tape first." "That's a δ problem."
- **Eps (ε), the son.** Early twenties, runs the scanner and the CAD, 1.70 m.
  - Quick, curious, impatient, funny. He asks *what and how*, reads customer questions aloud, and does the hands-on work.
  - His mistakes are only about patience and order of operations, never about specs.
  - Look:
    - a backwards cap with a brim shaped like a front lip;
    - a hoodie with a diffuser-strake detail on the hem;
    - a dark visor with two light-up eye marks: expressions come from the eye shape and the marks pulse when he talks, so no lip-sync.
  - Props: a handheld 3D scanner (laser blue is his colour), the configurator tablet, and a 10 mm socket he always loses.
  - Lines: "Okay but what if we scan it?" "Customer asks…" "Exploded view!" "Where's my 10 mm?"
- **Motto:** "For every ε, there's a δ."
- **Running gag:** Eps loses his 10 mm and Del has it in his pocket. Usable as an end sting.

### Rules for using them with our scans (from v0.1)
- **Same material as the car.** v0.1 shows them in the house silver on black, with the car the brightest thing in frame.
- **Real scale, real positions.** Built at 1:1 and placed in the car scan's registered space, so a hand on a fender is really on it.
- **They scan in.** Their entrance is the laser sweep building them from wireframe to silver; the exit is the reverse.
- **Parts move the way they unbolt.** If there's no removed-state scan, they don't remove it.
- **Micro mode.** About 1:10 for exploded views and drill points: Eps standing on an endplate, Del on a strake.
- **Cheap to animate.** Under 15k tris each, one shared rig, and a small action set: point, lift, hold up to camera, tape, drill, shrug, high-five.

### Colour (v0.2)
v0.2 puts the colour on the characters and keeps the scans silver. It offers three looks:
- **A: Team Livery.** Del in petrol teal #0f5c63 with signal orange #ff7a1a; Eps in electric violet #6b3cff with hi-vis yellow #ffd21f. A part washes violet while Eps handles it and orange while Del checks it. Best for installs.
- **B: Pressure Map.** CFD colour scales: Del warm (high pressure), Eps cool (fast flow). Show real pressure plots only when real CFD data exists.
- **C: Pit Crew Toys.** About 1:10 collectible figures standing on the parts. Best for FAQ, social and stickers.

The page recommends **A as the base, with B as a mode for aero moments.** The owner hasn't confirmed a pick: ask in your chat, or default to A and say that you did.

### Production paths (from v0.1)
- **Blender rig (recommended).** Most up-front work, but consistent.
- **AI video from character sheets.** A fast start, but weaker on contact with parts.
- **Stills composited into scan frames.**

For BF timing, propose the cheapest path that holds the look.

Search before you build. The research found no model or rig file yet, so check Drive and Dropbox for "Del", "Eps" or a turnaround; if none exists, the build is part of the plan. Use the Pip & Gus pipeline (Blender procedural build, Higgsfield voices) as the technical precedent, not their look.

## Confirmed BF prices (owner's doc "Black Friday 2026 Discounts: TL;DR")

Source: https://claude.ai/artifact/29kGfJ2WPdSAg5QpezXfva (2026-11-16). The detailed sheet is the "Black Friday 2026 Liquidation Pricing" artifact.

**Status:** the sale window (start and end dates/times) is NOT set yet, and nothing has changed on the site yet. Don't put dates on screen.

| Tier | Items | Example (was → BF) |
|---|---|---|
| 30% | PU front lips, side skirts, rear spats: Integra, Civic FE/FL Zenki + Kouki, Civic FE rear lip, Corolla HB, GR Corolla V2 + Kouki, Veloster N | Integra front lip $285 → $199.50 |
| 30%, base only | Sport Wings: Integra, Civic FL2/FL5, Civic FE sedan. The paint charge stays full price | Integra gloss black $500 → $350; painted $1,000 → $850 |
| Combo | Integra Sport Wing + Trunk Lip | **gloss black $600 → $385** (so the concept's "$750" is wrong; the was-price is $600) |
| 40–45% clearance | GR Corolla V1 lip (carbon 45%), V1 side skirts + spats, Integra rear spats, Evo 8 nose chop | GR V1 PU lip $215 → $129 |
| 50% | Integra fender flares | $800 → $400 |
| 60% deep clearance | Integra rear trunk lip, gloss black + carbon | ABS $100 → $40; carbon $240 → $96 |
| Flat clearance | FG2 Civic lip, VB WRX lip | $79.99 each |
| 20% | FRP + low sellers: MR2 parts, NC Miata bumper/fenders/skirts/spats/canards, MS3 flares, VB bumper (no fog), VB rear bumper, VB carbon skirts | VB rear bumper $1,500 → $1,200 |
| 10% | VB WRC wing (gloss; paint full price), all spoiler extensions | Extension $220 → $198 |

**Not on sale:**
- Autospec BRZ kit, GR Supra GT4 lip, GT wings, GT86 bumper, **MR2 front bumper**, Evo 8 OE replacement;
- VB fog-light bumper, VB ACM skirts, WRC carbon;
- anything on preorder or backorder;
- paint-match charges.

Customers will see the old price crossed out on the store.

**Stock watch-out (from the doc):** the VB lip, Integra trunk lip, Integra flares and some NC parts show negative inventory. Last year the BF window sold 33 front lips.

Use these figures on screen, and re-check any you show against the live store once the sale is live. "Only X left" still needs a real, positive count.
