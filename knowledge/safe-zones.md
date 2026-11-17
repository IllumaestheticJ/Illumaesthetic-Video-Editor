# Safe zones for 9:16 reels (owner rule, 2026-11-17)

The owner's instruction: "check that there isn't text or elements in the buffer zones (the bottom where comments are, the like button on the right side, the slight crop when going from home page to full screen etc)". This applies to every reel, from now on.

The rules use 1080x1920 pixels, and scale proportionally for other sizes. They combine the Instagram Reels, TikTok and YouTube Shorts layouts, so one master works on all three.

| Zone | Pixels | What covers it | Rule |
|---|---|---|---|
| Bottom | y > 1440 (bottom 480 px, 25 %) | caption, username, audio line, comment bar, CTA button | no text, logos, prices or key action |
| Right rail | x > 920, y 900-1440 | like / comment / share / remix / audio buttons | no text or logos; keep the subject's important detail clear |
| Top | y < 220 | status bar, "Reels / Following / For You" tabs, search | no text or logos |
| Left edge | x < 48 | edge margin | no text |
| Feed crop | y < 285 or y > 1635 | outside the centred 4:5 (1080x1350) preview shown in the home feed and profile grid, before the viewer taps to full screen | key text (offer, price, product name) and the hook subject stay inside 1080x1350 centred |

**So all text, prices, labels and logos sit inside x 48-920 and y 285-1440.** The safest band for a headline or price is y 400-1300. The car or part being sold should be framed so it reads in the 4:5 feed crop too.

## Check (part of the pre-delivery checks)

```
python scripts/safezone_check.py out.mp4 --every 0.5 [--text-boxes overlay_boxes.json]
```

The script writes `<out>_safezones.jpg`, a contact sheet with the zones tinted: red means app UI covers it, amber means outside the feed crop. **Look at the sheet**: no text or key element may touch red, and no offer or price may sit in amber.

If the edit's captions come from an overlay JSON or Remotion props, also export their boxes and pass them with `--text-boxes`. The script then fails (exit code 1) on any text box in a red zone, or on a box flagged `"key": true` in the feed crop.
