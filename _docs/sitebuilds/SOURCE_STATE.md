# Build-source state — READ BEFORE REBUILDING ANY SITE

**Written 2026-07-31 after a sandbox rollback.**

## What happened

Partway through 2026-07-31 the working sandbox reverted several hours of
**build-source** changes. The deployed sites were unaffected — every one of the
143 pages under `test-builds/` had already been pushed to this repo and is
correct and live. What was lost was the local `site_*.py` tree that generates
them.

`src/` in this directory is the surviving source tree, committed here so the
same loss cannot happen silently again. **Commit sources to this repo at the
end of every working session.**

## Which builders are trustworthy

| Builder | State |
|---|---|
| `site_hickey.py` + `site_hickey_build.py` | **current** — matches what is deployed |
| `site_dorfman.py` | **current** |
| `site_millcity.py` | **current** |
| `site_goguen.py` | **STALE** — predates the rework. Still contains the left `reach()` rail, the calculators and British spellings, none of which are in the deployed site. Partially re-fixed after the rollback (calculators and photographs), but not verified against the deployed output. |
| `site_carella.py` | **STALE** — predates the conventional-shell rework. Rebuilding from it would undo the top bar, the hero and the 1360px breakpoint fix. |
| `site_masstaxpros.py` | **MISSING** — never recovered |
| `site_kpw.py` | **MISSING** — never recovered |
| `contrast_masstaxpros.py`, `contrast_kpw.py`, `assets_masstaxpros.py`, `assets_kpw.py` | **MISSING** |
| `art.py` | **STALE** — the Mill City, Goguen, Mass Tax Pros and KPW plates are missing from `ART` |
| `calculators.py` | **STALE** — predates the presentation/arithmetic split (`dress()`) |
| `gates_bespoke.py` | **STALE** — missing the `masstaxpros` and `kpw-cpa` entries, and the Carella container contract |

## The rule this establishes

> **`test-builds/` in this repo is the source of truth for what is shipped.**
> A builder is only trustworthy if its output matches what is deployed.

Before rebuilding any site from `src/`, diff its output against
`test-builds/<slug>/`. If they disagree, the deployed version is correct and
the builder is stale — fix the builder, never overwrite the deployment with
builder output you have not checked.

For `masstaxpros`, `kpw-cpa`, `carellacpa` and `bgoguen`, the practical path is
to reconstruct the builder from the deployed HTML, which is complete and
passes every gate. Do not rebuild them from the stale builders.

## What is definitely intact

- All 143 deployed pages, all seven sites, all correct.
- `HANDOFF_SITE_BUILDS.md`, `BUILD_SPEC.md`, `CAMPAIGNS_SIX_FIRMS.md`.
- `dupcheck.py`, `british_check.py`, `british_fix.py`, `shot.py`.
- All seven Smartlead campaigns, live, sending Tuesday 4 August.
- `src/static/bgoguen/img/team/` — the five team photographs the firm supplied.
