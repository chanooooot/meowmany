# Cat upgrade QA

Identity reference: original orange tabby idle frame, extracted with sprite-gen
slice-sheet from the existing embedded atlas. Garden art remains the approved design.

GPT generated each state as a separate row. Walk took four passes: repeated
contact poses in the earlier rows were rejected. The accepted row additionally
references `../paw-guide.png`, made by `../motion-reference.py`; this schematic
owns leg placement only. The original base owns all colors and character details.
Generation reports preserve the references and prompt used.

- Scared: pose/identity pass. Runtime holds frame 2, with flattened ears, wide
  eyes, a crouch, and puffed tail. The held frame fits entirely inside its cell.
  Other scare source frames include tight margins; they are not animated at runtime.
- Happy: pose/identity pass. Four curled, closed-eye poses with subtle breathing;
  first/last silhouettes agree. Runtime raises the cat 16px onto the existing
  cushion. `../rest-on-bed.png` verifies asset placement independently of the UI.
- Walk: best-effort motion verdict from frame progression. Near/far front paws
  alternate between the two contact phases; four poses maintain head/body scale
  and a common baseline. `../fit-walk.py` applies the same 1.3 scale and -16px
  vertical offset to every frame through canonical sprite-gen curation, restoring
  the original walking footprint. It does not redraw poses or change timing.
  Exported GIF is 10fps, matching the shipped 400ms travel/animation cycle.

Extraction, composition, curated PNG/GIF export, and inspect report succeed.
Extractor warnings about a harmonic pitch detection are resolved by row consensus.
Scare silhouette similarity warning is expected from the deliberate crouch.
Shipped idle row is pixel-identical to the original; all new cells are 130x120.
The page remains self-contained; no gameplay/audio thresholds or logic changed.

`node tools/test-game.cjs`: 23 checks pass. Build verifies valid frames and idle
preservation. GIFs and contact sheets are available for manual animation review.
Browser URL policy blocked opening the local page. Live temporal continuity and
updated mobile/landscape UI rendering have not been verified in a browser or on
an actual phone; the walk remains best-effort until that visual gate is complete.
