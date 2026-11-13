# Graph Report - miata-bracing-longform  (2026-11-13)

## Corpus Check
- Corpus is ~22,312 words - fits in a single context window. You may not need a graph.

## Summary
- 204 nodes · 452 edges · 9 communities
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 42 edges (avg confidence: 0.88)
- Token cost: 121,332 input · 0 output

## Community Hubs (Navigation)
- 3D Heat Maps and Scan Maths
- Independent Review Findings
- Timeline, Script and Callouts
- Graphics Plan and Scan Data
- Motion Graphics Layer
- Data Cards
- Measurements and Scan States
- Final Assembly: Voice and Music
- Chassis-Flex Intro Graphics

## God Nodes (most connected - your core abstractions)
1. `Independent review: MiataBracing_review_v2.mp4 (agent_review.md)` - 22 edges
2. `CGI and graphics plan (graphics_plan.md)` - 12 edges
3. `Script and edit plan v5 (script.md)` - 12 edges
4. `Sign-off pass on v3 (not approved yet)` - 11 edges
5. `Strut Spread.xlsx (engine-bay width per state)` - 11 edges
6. `Fx` - 10 edges
7. `Miata chassis-bracing long-form notes (clips.md)` - 10 edges
8. `F()` - 9 edges
9. `F()` - 8 edges
10. `Strut-top spread cross-check (local trimmed ICP)` - 8 edges

## Surprising Connections (you probably didn't know these)
- `New narration: 1012 words at 2.6 words/s` --conceptually_related_to--> `B6: line lengths assume 2.9 words/s, voice clone reads 2.2`  [INFERRED]
  script.md → agent_review.md
- `Burned-in rough-cut titles over IRL footage` --semantically_similar_to--> `Review captions over IRL footage (draft narration, temporary)`  [INFERRED] [semantically similar]
  agent_review.md → review.md
- `CGI and graphics plan (review proposal, 10 items)` --semantically_similar_to--> `CGI and graphics plan (graphics_plan.md)`  [INFERRED] [semantically similar]
  agent_review.md → graphics_plan.md
- `v3 problem: strut-top cross-check undercuts unqualified conclusion lines` --references--> `Strut-top spread cross-check (local trimmed ICP)`  [INFERRED]
  agent_review.md → clips.md
- `Body percentages (58/60/91/74) must be disclosed as our own calculation` --references--> `Body-only deviation stats table (median, p90, within 2.5/5 mm)`  [INFERRED]
  agent_review.md → clips.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Five scan states of the bracing test (control + four jacked)** — clips_control_scan, clips_jacked_no_bracing, clips_fender_braces_only, clips_strut_tower_brace_only, clips_fender_plus_strut [EXTRACTED 1.00]
- **Conflicting tower-spread measurements that block ranking the braces** — clips_strut_spread_xlsx, agent_review_distance_measurement_pdf, clips_strut_top_spread_cross_check, agent_review_b1_second_tower_measurement, agent_review_strut_top_cross_check_undercuts [INFERRED 0.85]
- **Story order: control -> fender -> strut -> both -> conclusions** — script_section_1_control, script_section_2_fender_braces, script_section_3_strut_tower_brace, script_section_4_both_braces, script_section_5_conclusions [EXTRACTED 1.00]

## Communities (9 total, 0 thin omitted)

### Community 0 - "3D Heat Maps and Scan Maths"
Cohesion: 0.10
Nodes (18): _ramp(), cmap(), load(), pair(), prep(), render(), state(), cmap() (+10 more)

### Community 1 - "Independent Review Findings"
Cohesion: 0.13
Nodes (32): Independent review: MiataBracing_review_v2.mp4 (agent_review.md), B1: second tower measurement disagrees (+0.691 vs +0.237 mm), B2: ranking and mechanism claims the data does not support, B3: whole-body heat-map claims asserted from maps showing panels and alignment, B4: wrong burned-in title in the fender-only section (5:09), B5: rough-cut 'How to read the heatmaps' legend card contradicts what follows, B6: line lengths assume 2.9 words/s, voice clone reads 2.2, Body percentages (58/60/91/74) must be disclosed as our own calculation (+24 more)

### Community 2 - "Timeline, Script and Callouts"
Cohesion: 0.10
Nodes (17): Grimace tracked arrow + label callout, Intro and setup (existing voice, new graphics, callouts), Miata Chop Shop label, ass(), at(), build(), chunks(), dur() (+9 more)

### Community 3 - "Graphics Plan and Scan Data"
Cohesion: 0.13
Nodes (20): Burned-in rough-cut titles over IRL footage, CGI and graphics plan (review proposal, 10 items), Heat-map gate: reproduce the unbraced report pattern within ~2 mm first, Non-blocking issues (picture vs words, cards), Exterior STLs exported already aligned to the control: do NOT re-ICP, Scan-driven heat maps (tested 2026-11-12), Tower close-up maps show no braced-vs-unbraced difference, CGI and graphics plan (graphics_plan.md) (+12 more)

### Community 4 - "Motion Graphics Layer"
Cohesion: 0.27
Nodes (6): a8(), ease(), F(), Fx, _logo(), spring()

### Community 5 - "Data Cards"
Cohesion: 0.22
Nodes (13): bullets(), F(), fit(), frac(), page(), pair(), renumber(), table() (+5 more)

### Community 6 - "Measurements and Scan States"
Cohesion: 0.24
Nodes (17): Terminology: 'control' vs 'no bracing' instead of 'stock', Body-only deviation stats table (median, p90, within 2.5/5 mm), Control scan (on the ground, 960.948 mm), Fender braces only (961.185 mm, +0.237, 86 % reduction), Fender + strut braces (961.384 mm, +0.436, 74 % reduction), Jacked, no bracing (962.643 mm, +1.695), Strut Spread.xlsx (engine-bay width per state), Strut tower brace only (961.679 mm, +0.731, 57 % reduction) (+9 more)

### Community 7 - "Final Assembly: Voice and Music"
Cohesion: 0.16
Nodes (7): act_rms(), fitted(), level(), spectrum(), tone(), trim(), wav()

### Community 8 - "Chassis-Flex Intro Graphics"
Cohesion: 0.33
Nodes (10): arrow(), ease(), frame(), P(), loads(), proj(), tub(), line() (+2 more)

## Knowledge Gaps
- **6 isolated node(s):** `Voice analysis vs owner transcript (So/actually/just tics, missing questions)`, `House rules to confirm (voice clone consent, imperial units)`, `#7 House 1:1 hard cut from static front shot to control scan`, `Miata Chop Shop label`, `Takeaways card` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 36 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Independent review: MiataBracing_review_v2.mp4 (agent_review.md)` connect `Independent Review Findings` to `Timeline, Script and Callouts`, `Graphics Plan and Scan Data`, `Measurements and Scan States`?**
  _High betweenness centrality (0.172) - this node is a cross-community bridge._
- **What connects `Voice analysis vs owner transcript (So/actually/just tics, missing questions)`, `House rules to confirm (voice clone consent, imperial units)`, `#7 House 1:1 hard cut from static front shot to control scan` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `3D Heat Maps and Scan Maths` be split into smaller, more focused modules?**
  _Cohesion score 0.1021021021021021 - nodes in this community are weakly interconnected._
- **Why does `CGI and graphics plan (graphics_plan.md)` connect `Graphics Plan and Scan Data` to `Independent Review Findings`, `Measurements and Scan States`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Should `Independent Review Findings` be split into smaller, more focused modules?**
  _Cohesion score 0.1310483870967742 - nodes in this community are weakly interconnected._
- **Why does `Script and edit plan v5 (script.md)` connect `Independent Review Findings` to `Timeline, Script and Callouts`, `Measurements and Scan States`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Should `Timeline, Script and Callouts` be split into smaller, more focused modules?**
  _Cohesion score 0.0967741935483871 - nodes in this community are weakly interconnected._