# Epsilon+ Wing Configurator: feature inventory

Source of truth: the live app at `https://epsilon.plus/pages/wing-configurator` (script `epsilon-wing-configurator-0.9.18.js`),
explored with Playwright + Chromium on 2026-11-12 (desktop 1600x1000 and portrait 540x960 / 720x1280 / 1080x1920 viewports).
Supporting text: the launch post `https://epsilon.plus/blogs/news/epsilon-wing-configurator-beta` (Sep 30, 2026, written
for version 0.8; where the post and the live app differ, the live app wins and the difference is noted).
"Seen" = where the control/feature was observed. Nothing below is inferred from marketing copy alone unless marked (blog only).

## Layout
| Feature | Seen |
|---|---|
| Page "WING CONFIGURATOR": car view (stage) left, "Configure your wing" panel right (desktop); panel becomes a bottom sheet on phones | live, all viewports |
| Panel header: car name + wing + live "Est. $" price; minimise/open toggle ("CONFIGURE" on phones) | live, `.ewc-drawer-head` |
| Four numbered steps: 1 Vehicle, 2 Wing, 3 Setup, 4 Price & quote | live panel |

## 1 Vehicle
| Feature | Seen |
|---|---|
| Make dropdown: 15 makes (Acura, BMW, Chevrolet, Ford, Honda, Hyundai, Infiniti, Lexus, Mazda, Mitsubishi, Nissan, Porsche, Subaru, Toyota, Volkswagen) | live `select[aria-label=Make]` |
| Model dropdown with years and model kind: 72 models total, **45 "3D Scan"**, 15 "Hybrid Model", 12 "Game Model" (full list: `/home/user/media/epsilon-wing-configurator/web/cars.json`) | live, iterated every make |
| Blog says 49 cars / 12 makes / 40 scans at launch (v0.8) - outdated; reel uses the live counts | blog only |
| The 3D view swaps to the chosen car's model (scan / hybrid / game) | live |

## 2 Wing
| Feature | Seen |
|---|---|
| Wing element: TC 47.5" (1206 mm), TC 66.5" (1689 mm), GT Wing (66 Inch, Dry Carbon), Custom TC width... | live `select[aria-label="Wing element"]` (also in the Rear view toolbar) |
| Custom TC width: made-to-order width field ("Made to order, min to max") | live option + help-text table in JS |
| GT wing "comes in one width" | JS help text `hint.wingWidth` |

## 3 Setup
| Feature | Seen |
|---|---|
| Setup cards: the car's tested/standard setups, one tagged RECOMMENDED (e.g. GR86: Bottom mount 12.5RR sheet-metal base; Swan neck BRZ Swan Short / Tall; Swan neck Type A Swan CNC base. Miata NA: Bottom mount 6.5" Shorty; Fender mount NA Miata fender mount upright) | live `.ewc-presets` on GR86, NA Miata, FL5, VA, S2000, A90, 350Z, C8 |
| RESET TO RECOMMENDED | live |
| "Adjust: mount, upright, base, exact position" expander | live `<details>` |
| AoA hole: 16 holes (0-15), 1 deg per hole, shown as the wing angle to the ground (e.g. GR86 hole 0 = -0.6 deg ... hole 15 = -15.6 deg) | live `select[aria-label="AoA hole"]` |
| Mount: Bottom mount / Swan neck / Fender mount (fender only where a fender kit exists, e.g. NA Miata) | live `.ewc-seg` |
| Upright picker with fit status ("Fits"), "Best match for my wing position", grouped lists: bottom-mount uprights (6.5" Shorty, 10.5", 11.5", 12.5", 12.5R, 12.5RR), swan necks (S2000 / NA / FRS / BRZ Swan Short and Tall, car-specific swans like Civic Type R, Supra A90 GT4, C8 Corvette, Type A/B CNC swans) | live `.ewc-dd` |
| Base style: 5 AXIS CNC or SHEET METAL WELDED/BENT (N/A where not made), "Change" / "Reset to default"; base name (e.g. BRZ/GR86 (ZD8) base) | live (GR86; Miata shows CNC N/A) |
| Base position: Forward, Spacing, "Reset bases" | live (GR86 bottom mount) |
| Exact numbers, each with -/+ buttons, slider and typed value: Overhang past the bumper; Upright height, hole to hole; Upright spacing, centre to centre; Wing angle to the ground (endplates' flat) | live `.ewc-numctl` |
| Locks "Keep while the wing moves": Upright, Base, Width, Upright angle | live `.ewc-lockgrid` |
| Custom mode: moving the wing off a tested setup designs a new upright ("New bottom-mount upright (from 12.5RR)") and adds "Custom uprights (pair) +$200"; moving bases adds "Custom bases (pair) +$200" | live, GR86 side-view drag |
| Fit checks: issues in red, warnings in amber, hard limits ("The wing stops ... above the roof"), hatch/visual-only notes | JS help text table (`stage.issue` etc.); not triggered in capture |

## Views (stage)
| Feature | Seen |
|---|---|
| 3D: drag to turn the car, scroll/pinch to zoom (view only) | live |
| SIDE: line drawing of the car with OVERHANG and HEIGHT dimensions; drag the wing to move it, drag the round handle to tilt it; TRUNK / WHOLE CAR zoom | live |
| REAR: UPRIGHT SPACING C-C dimension, wing element picker; drag an endplate to change the width, drag a base to change the spacing | live |
| MM / IN units toggle | live |
| HANDLES on/off | live |
| Undo / Redo (Ctrl+Z / Ctrl+Shift+Z) | live |

## 4 Price & quote
| Feature | Seen |
|---|---|
| Summary: Car, Wing, Mount | live |
| Price table with kit price, custom fees, Total; header "Est." price updates live (e.g. GR86 TC 66.5" bottom mount $850; + custom uprights $1,050; + custom bases $1,250; Miata swan neck $1,100) | live |
| REQUEST A QUOTE: locks the build ("Unlock and edit") and opens the quote form with SEND QUOTE REQUEST (never submitted in this project) | live |
| SAVE SPEC: "Saved. Link copied." + "Link to this spec" (stored in the browser, list of saved specs) | live + JS |
| DETAILS: setup, upright + plate thickness, height, overhang, spacing, base (hole height, plate bend), AoA | live |
| Blog's "download the spec and drawing" / "add it to your cart": not offered to public users in 0.9.18 (download buttons are behind an admin flag in the JS); not claimed in the reel | JS + blog |

## More options / support
| Feature | Seen |
|---|---|
| Add a car from a blueprint (image upload) | live "More options" |
| Use your own photos: side photo + rear photo upload | live "More options" |
| Report a problem: category (Wrong fit or position, Model looks wrong, Missing car, Price or cart, Other), message, optional email (never submitted) | live |
| Beta notes: positions are a guide, not a drill template; some combinations visualisation only | blog + JS help text |

## Coverage in the reel (v1)
| Feature | In the reel? | Shot / time | Why |
|---|---|---|---|
| Make/Model + 3D Scan/Hybrid/Game labels, 72 cars / 45 scans | yes | cars 8.6-14.1 (spoken) | core step; counts from the live list |
| Wing element: TC 47.5 / TC 66.5 / GT dry carbon / custom width | yes | wing 14.1-18.0 | step 2, every option shown |
| Tested setup cards (+RECOMMENDED), Mount: bottom / swan neck / fender | yes | mounts 18.0-24.1 (NA Miata) | the only car checked with all three mounts |
| Base style CNC vs sheet metal | yes | bases 24.1-26.1 (GR86) | |
| AoA holes 0-15, 1 deg per hole | yes | aoa 26.1-29.1 | |
| 3D view drag/zoom | yes | turn3d 29.1-30.6 | |
| Side view: drag wing (overhang/height), tilt handle; custom upright +$200 | yes | side 30.6-35.6 | |
| Rear view: endplate drag -> width (snaps TC 47.5, Est. $800) | yes | rear 35.6-38.6 | |
| Number controls (sliders, +/-), locks, MM/IN | yes | sliders 38.6-43.1 | |
| Live estimate, price table, Save spec (link), Request a quote (lock) | yes | price 43.1-48.7 | quote never sent |
| More options: blueprint / own photos | yes | more 48.7-52.6 | nothing uploaded |
| Phone layout (CONFIGURE bottom sheet) | yes | hero_b 4.1-8.6 | shows the 4 steps + estimate header |
| Reset to recommended, Base position (Forward/Spacing/Reset bases), upright picker list, TRUNK/WHOLE CAR, HANDLES, Undo/Redo, Details | on screen, not narrated | various | visible in frames; narration kept tight |
| Fit issue/warning messages | no | - | not triggered by any tested setup; would need a forced bad fit |
| Report a problem | no | - | support form, not a configuration feature (visible at the bottom of the more-options panel) |
| Spec/drawing/DXF downloads | no | - | admin-only in 0.9.18 (not public); blog's claim not shown |

## v2 changes
- More options (blueprint / own photos): **removed** from the reel (user). Still in the app.
- Base style now shown with the tested setups (Swan Tall sheet metal vs Type A Swan CNC) instead of forcing CNC on a bottom mount.
- Ending adds real customer cars (epsilon.plus TC-wing product galleries: GR86 c216, S2000 c017, NA Miata c163, NB Miata c065) and the call to action "Try it now on epsilon.plus".
