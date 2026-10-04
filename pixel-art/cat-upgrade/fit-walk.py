"""Apply one uniform size/foot-anchor correction using sprite-gen curation."""
from pathlib import Path
from sprite_gen.curate.curation import run_revision, state_revision, write_curation_atomic

run = Path(__file__).resolve().parent / "run"
write_curation_atomic(run, {
    "version": 1,
    "kind": "sprite-gen-curation",
    "run_revision": run_revision(run),
    "states": {
        "walk": {
            "revision": state_revision(run, "walk"),
            "selected": [0, 1, 2, 3],
            "transforms": {str(frame): {"scale": 1.3, "dy": -16} for frame in range(4)}
        }
    }
})
