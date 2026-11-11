# scary-shorts

Daily animated folklore Shorts.

- `setup.sh` – installs the voice model and packages
- `toon.py` – cartoon drawing helpers (SVG)
- `stories/<id>.json` + `stories/<id>.py` – script and scenes for one story
- `make_short.py stories/<id>.json` – renders `videos/<id>.mp4` (`--preview` writes a contact sheet to `work/<id>/sheet.jpg`)
- `USED.md` – legends already used

## Animated characters ("actor" scenes)
Main characters must be rigged and animated, not static drawings. In a scene dict add
`actor=dict(box=(x0, y0, x1, y1), fn=lambda ts, t: <svg string>)`: `fn` is called every frame (`ts` = seconds since the scene
started, `t` = global time) and its SVG is drawn on top of `mid` and under `fg` (so trees/bars/windows in `fg` can hide it).
Rigs live in toon.py: `human(...)` (stand/walk/run/scared/reach/point, expressions, lantern) and `clown(...)` (walk/wave/face).
Both are skeletons made of nested transforms; copy their pattern for any new creature (ghost, beast, witch...).
Keep `box` as small as the character's movement allows (render cost). Per scene you can also set `"focus": [fx, fy]` (where the
close-up shots look, 0-1) and `"fog": false` (for interiors / extreme close-ups). See stories/005-phantom-clowns.py.
