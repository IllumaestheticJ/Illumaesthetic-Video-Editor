"""Headline font per knowledge/fonts.md: Akira (Expanded) if the owner's file is in assets/fonts/akira/,
else the Unbounded 800 stand-in. Text beside the logo never uses this (Unbounded 300/400 there)."""
import glob, os
R = "/home/user/Illumaesthetic-Video-Editor/assets/fonts"
_ak = sorted(glob.glob(f"{R}/akira/*[Ee]xpanded*.[ot]tf") or glob.glob(f"{R}/akira/*.[ot]tf"))
HEAD = _ak[0] if _ak else f"{R}/unbounded/Unbounded-800.ttf"
IS_AKIRA = bool(_ak)
