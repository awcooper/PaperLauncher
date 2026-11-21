# Paper Launch

A doodle-themed launching game in the spirit of Burrito Bison, Toss the Turtle and Kitten Cannon.
Originally my term project for 15-112 at Carnegie Mellon (Spring 2012), now playable in the browser.

## ▶ Play in your browser

**https://awcooper.github.io/PaperLauncher/**

Works on desktop and mobile. Your progress is saved in the browser (localStorage).

| Action | Keyboard | Touch / mouse |
| --- | --- | --- |
| Set power, set angle, boost | Space | Tap the screen |
| Navigate menus | Arrow keys + Enter | Tap the arrows / cards |
| Buy or equip in the store | Enter | Tap an item, then tap it again |
| Back | Esc | ← Back button |
| How to play | I | ? button |

### Run the web version locally

The web app is plain HTML, CSS and JavaScript with no build step:

```sh
cd web
python3 -m http.server 8000
# open http://localhost:8000
```

Pushing changes under `web/` to `master` redeploys the site automatically via
`.github/workflows/pages.yml`. (One-time setup: **Settings → Pages → Source: GitHub Actions**.)

## Desktop (Python) version

The original pygame version still works and now runs on Python 3:

```sh
pip install -r requirements.txt
python3 PaperLaunch.py
```

All navigation is done with the arrow keys and Enter; Space launches and boosts.
To use a custom background, put an image named `userbg` (at least 800px tall) anywhere
inside `PaperLaunchFiles/Images` and restart the game.

## Project layout

```
web/                 Browser version (index.html, style.css, js/game.js, assets/)
PaperLaunch.py       Desktop version (Python 3 + pygame)
PaperLaunchFiles/    Original art, save files and earlier prototypes
```

## Changes in 2026

Bug fixes in the Python version (all carried over to the web version):

- **Crash on Python 3.12+**: spawning a shark, cat or airplane after boosting crashed with
  `TypeError` in `random.randint` because positions became floats.
- **Crash when collecting money at the screen edge**: objects removed themselves from the
  list they were being iterated over and could be removed twice.
- **Distance earnings were lost**: the game saved *before* adding the run's distance money.
- **"Delete File" didn't delete**: it only reset memory (and kept the sketchbook, because the
  empty-save template was being mutated); it now writes a fresh save.
- **Couldn't leave Options**: Esc didn't work on the Options screen.
- **Nyan Cat animation** only ever showed two of its four frames (`if` instead of `elif`).
- **Boot names were swapped** relative to the store icons and descriptions.
- Boosting was still possible on the game-over screen.
- Best height is now saved; old save files missing keys are upgraded instead of crashing.
- Paths are resolved relative to the script, so it runs from any directory.

Cleanup: shared hitbox/collision/sketchbook code moved into the base class, the main loop is
in `main()`, dead code removed.

The web version adds touch controls, responsive scaling, fullscreen, best-distance tracking,
clearer store feedback (affordability, "equipped", "Purchased!"), and a fixed 30 Hz simulation
so it plays at the original speed on any monitor.

## Credits

Game and most art by Adam W. Cooper. Additional doodles by Audrey Wu (Nyan Cat), Connie Dai
(airplane), Dan Cushman (shark), Faith Quist (bear, Hermes boots) and Hira Ahmad (car, money).
