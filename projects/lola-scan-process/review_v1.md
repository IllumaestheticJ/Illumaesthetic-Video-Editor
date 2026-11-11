# Lola (Drifter movie) scan-process reel v1 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/lola_scan_process_v1.mp4`. Specs: 1080×1920, 30 fps, yuv420p, AAC, 31.97 s (959 frames). Music: the parent session's track, fading out with the logo.

> ⚠️ **Before publishing:** these cars (Lola 1 and Lola 2) were scanned for a **film production
> (Drifter)**. The user must confirm we are allowed to post this footage and the scan data before
> it goes public.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Powder-spray sweep over the real car from frame 0. The 1:1 real→scan transformation lands on the drop at 2.43 s. It isn't first-1.5 s, because the drop sits at 2.43 s in the track. |
| 2 | Beat sync | 5 | 11 cuts on measured 40–120 Hz kick peaks. On the delivered file they measure −13 to +9 ms off the kicks (all within ½ frame). |
| 3 | 1:1 match | 5 | Two hard 1:1 cuts, both checked with onion overlays and the actual cut frames. A (spray → Lola 1 exterior) is on the drop, with silhouette refine at fx 1094. B (handheld scanner → explode) is on the lift, solve RMSE 5.2 px, and roofline, C-pillar, wheel and door seam overlap. |
| 4 | Scan quality | 4 | Silver on black. Lola 1 exterior/interior is clean. The Lola 2 close-ups use the 4 mm decimation (memory limit on the 50M-triangle file), so the surface is a little soft and there are small holes inside the pop-up housings. |
| 5 | Story | 4 | Sequence: real car → sprayed → becomes the scan → crew with the handheld scanner → becomes the scan, the shell lifts off the interior/cage scan and spins → cabin scanning → software registration → Lola 2 sprayed → Lola 2 colour model → silver details → logo. There is no product listing, so the reel ends on the brand card. |
| 6 | Grade | 4 | The glasses footage is SDR and consistent. The two screen recordings are flat by nature. |
| 7 | Text | 5 | Only STL triangle counts from the files (21,696,194 / 25,188,507 / 49,997,072) plus labels. Shown only on scan shots, never over IRL. Counter shortfall found and compensated (see editlog). |
| 8 | Ending | 5 | Logo on the last hit at 28.73 s; ILLUMAESTHETIC.COM fades in last; picture and music fade together and the reel ends where the track ends. |
| 9 | Technical | 5 | 1080×1920, 30 fps, yuv420p, AAC. No black or duplicate frames at cuts (frame-diff scan of every cut). |

## Deviations from the brief
- **No third 1:1 cut on Lola 2.** The steep, close glasses view of the rear wing didn't converge, so Lola 2 shows as real → software colour model → silver details instead.
- **No separate part scans exist.** The "explode" uses Lola 1's exterior scan lifting off its interior scan, rotating 360°.
- **No illumaesthetic.com listing for Lola.** The only AE86 product is a DIY kit, which is a different product, so the reel ends on the logo card with ILLUMAESTHETIC.COM.
- **Hook timing.** The 1:1 sits on the drop at 2.43 s, as the parent asked, not inside 1.5 s.

## v2 ideas
- Render the Lola 2 close-ups from a 2 mm crop of just the front/wing region (fits memory) for sharper detail.
- The s3 hero frames the car slightly right of centre (bumper corner clipped). Re-aim 0.2 m left.
- Fix `remotion/src/ScanHUD.tsx` Counter easing so it ends on the exact value. The compensation in overlay.json then has to come out.
