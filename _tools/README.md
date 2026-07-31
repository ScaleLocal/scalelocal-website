# ScaleLocal — CPA spec-build tooling

Everything needed to build, verify and ship the demo sites. **Read
`HANDOFF_SITE_BUILDS.md` first** — it carries the mission, the hard standard, the
deployment method and the traps.

## The rule that matters most

Every site is designed and built from scratch with its own layout architecture. A
shared template reskinned in different colours is not an acceptable deliverable.
`site_hickey.py` + `site_hickey_build.py` are the reference for what clears the bar —
read them for *shape*, then design something genuinely different.

## Layout

    qa.py contrast.py layout_audit.py shots.py   verification harness (firm-agnostic, REUSE)
    calculators.py                               8 native calculators, formulas node-verified
    render_assets.py                             og.png + apple-touch-icon per firm
    extract_prose.py                             pull verified prose out of built/deployed pages
    site_hickey*.py                              BESPOKE reference build (no shared layout)
    build.py design.py content_*.py firms/       RETIRED template engine — do not seed new sites
    research/<slug>.md                           verified facts + explicit do-not-claim lists
    content_blocks_hickeycpa.json                extracted prose for the Hickey rebuild

## Verify (all four must be clean before shipping)

    BUILD_FIRM=<slug> python3 qa.py            # RESULT: PASS, 0 fails AND 0 warnings
    BUILD_FIRM=<slug> python3 contrast.py      # FAILS: 0
    BUILD_FIRM=<slug> python3 layout_audit.py  # GATE A + GATE B/C PASS
    BUILD_FIRM=<slug> python3 render_assets.py

`qa.py` reads `ALLOWED_PHONES` / `BANNED` and `contrast.py` reads `T` from
`firms/<slug>.py` — keep that file present with those three even for a bespoke site
that never imports the engine.

Then **look at screenshots**. Gates pass on things that look broken to a human.
