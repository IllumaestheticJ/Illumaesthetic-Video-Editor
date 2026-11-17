# Endings: reassembly, logo, store CTA

## Which ending

| Reel | Ending |
|---|---|
| Scan reel whose scan is sold on illumaesthetic.com | Reassembly lands 1:1 on the listing's cover photo, then zooms out to the **mobile** product page ("scan data now available"), then the logo |
| Scan reel with no listing | Reassembly, fade, logo |
| Epsilon kit reel (Civic 11, MR2 Spyder) | Kit installed, 1:1 cut to a Ron render, or to a real or CGI drive, then the **Epsilon** wordmark, not Illumaesthetic |
| Engineering / service reel (GR Corolla) | Logo plus contact line ("contact us for your engineering/scanning needs" + website), `projects/toyota-gr-corolla/tools/endcard.py` |
| Partner build (Frontier, QX80, 400Z) | Partner logos as the user supplied them (MotoIQ: red square around "IQ" only), with no slogans ("Get rid of 'Customize everything'") |
| Film (Lola) | No website URL, no festival caption |

## Logo

- 640-760 px wide on a 1080 frame, with 720 px as the default. Every reel delivered at 270-460 px got "logo too small".
- Put it on a downbeat and fade the audio with it. Keep it short ("takes too long", Civic 11).

## Store CTA (the "240SX-style" ending)

1. Get the product page for the car's scan on illumaesthetic.com. Capture it with Playwright at iPhone 13 size, and use the
   cover photo.
2. Frame the last reassembly shot so the car matches the cover photo's camera. That's a 1:1 match: solve it the same way
   as the IRL match cut (`knowledge/match-cut.md`).
3. Hard-cut or dissolve into the photo, then zoom out to the phone-framed page. The WebZoom component has mobile layout props.
4. Keep the text high on the frame, because phone UI covers the bottom. Change the dropdown and price only in the video,
   never on the site.
5. Theme colours are the site's own CSS variables: bg #0b0c0b, accent #619f73, text #f2f3f1. Headings are Fjalla One caps;
   body text is Barlow.

Reference builds:
- `projects/mazda-miata-na` (v3-v5);
- `projects/ferrari-296` (v6-v9, the dropdown that follows the photo);
- `projects/porsche-gt3-vs-gt3rs` (v3, two listings).
