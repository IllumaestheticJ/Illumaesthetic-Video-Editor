# BF prices: the source of truth (owner decision, 2026-11-17)

The owner's instruction: **"tell all BF agents to use the BF liquidation spreadsheet ... even if the stock is not right."**

- **Source.** Prices come from the Claude Sheet "Black Friday 2026 Liquidation Pricing" (https://claude.ai/artifact/BSCEWTDHHKuC9Yop5xh2X6), tab **Pricing**. A snapshot taken at revision 25 on 2026-11-17 is in `bf_liquidation_pricing.csv` next to this file.
- **Read the live sheet when you can.** If the sheet has changed since this snapshot, the live sheet wins. Re-read the Pricing tab before you finalise any on-screen number, using the Claude Docs connector:
  1. Read the doc with `ref {"object":"project","id":"547fe743-00d0-4861-be87-2ad106f972e5"}`.
  2. Read the cells with `ref node 05970616-f01e`, `engine "workbook"` and payload `{"kind":"readCells","sheet":"Pricing","range":"A1:Q108"}`.
- **Use the price on the sheet even when the store shows negative or backordered stock.** The owner overrode the "no backorder items" rule. Only items the sheet itself prices at 0% ("No deal") are off sale.
- **Never put a stock count or "only X left" on screen unless the owner asks for it.**
- **Use the "Current Price" column as the crossed-out price**, and "BF 2026 Price" as the sale price.

## The figures the BF videos use (from the snapshot)

| Item | Was | BF |
|---|---|---|
| Integra DE4 front lip PU | $285 | $199.50 (30%) |
| Integra DE4 side skirts PU | $400 | $280 (30%) |
| Integra DE4 rear spats PU | $175 | $105 (40%) |
| Integra fender flares | $800 | $400 (50%) |
| Integra Sport Wing gloss | $500 | $350 |
| Integra Sport Wing paint-matched | $950 | $800 (base discount only) |
| **Integra Sport Wing + Rear Trunk Lip, gloss** | **$600** | **$385** |
| Integra Sport Wing + Rear Trunk Lip, paint-matched | $1,050 | $835 |
| Integra rear trunk lip ABS gloss / carbon / painted | $100 / $240 / $300 | $40 / $96 / $240 |
| Civic FE/FL front lip (Zenki and Kouki) PU | $285 | $199.50 |
| Civic FE/FL side skirts PU | $400 | $280 |
| Civic FE rear lip PU | $285 | $199.50 |
| Civic paint-matched lip / skirts | $485 / $800 | $399.50 / $680 |
| Civic FL hatch rear lip (pre-order) | $285 | no deal |
| Sport Wing Civic FL2 / FL5 / FE (gloss) | $450 | $315 |
| Sport Wing Civic FL / FE paint-matched | $850 | $715 |
| GR Corolla V2 lip / skirts / spats PU | $285 / $400 / $175 | $199.50 / $280 / $122.50 (30%) |
| GR Corolla V1 lip PU / carbon | $215 / $600 | $129 (40%) / $330 (45%) |
| GR Corolla V1 skirts / spats PU | $275 / $125 | $165 / $75 (40%) |
| FG2 Civic lip PU | $150 | $79.99 |
| WRX VB lip PU | $99.99 | $79.99 |
| MR2 duckbill | $220 | $176 (20%) |
| MR2 eyelids / hood vents (vents only, with brackets) / rear spats / side skirt + fender combo | $100 / $400, $470 / $350 / $700 | $80 / $320, $376 / $280 / $560 (20%) |
| MR2 front bumper | $900 | no deal |
| NC Miata bumper + lip / top only / lip only | $1,100 / $800 / $350 | $880 / $640 / $280 (20%) |
| NC fender cuts / with fin, side skirts, NC1 rear spats, canards | $300 / $350, $500, $250, $200 | $240 / $280, $400, $200, $160 (20%) |

Other figures in the sheet:
- **Lip Kits tab:** a kit bought together is 10% off the regular total, but parts bought separately at BF prices come out cheaper. Don't feature "kit price" deals.
- **Rules tab:** paint-match charges stay at full price.
- **Free gift:** the Epsilon Basic T-shirt is suggested as a free gift on orders over $250, but this is a suggestion only. Ask the owner before showing it.

**Sale end date: NOV 30 (owner, 2026-11-18, via BF10).** Use "UNTIL NOV 30" or "ENDS NOV 30". The start date and the end time of day are still not set, so put no start date or time on screen.
