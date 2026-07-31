# Airbourne Arena repository contract

Use this reference whenever `Anharmoniclabs/airbournearena` is the target.

## Product and canon

- Product: mobile-friendly 4v4 browser air-combat game with a six-chapter, 32-mission campaign.
- Live game: https://anharmoniclabs.github.io/airbournearena/
- Canon: `docs/STORY-BIBLE.md`. Do not invent or overwrite faction, character, campaign, or ending facts without explicit approval.
- Core pillars include fast entry into flight, focused open regions, meaningful team selection, aircraft-build tradeoffs, morally complex factions, reuse of gameplay systems, and importance earned through player skill.

## Source and generated files

The deployable browser game is intentionally one shared-scope HTML file so it can run from `file://` and GitHub Pages.

- Edit: `Airbourne-Arena/src/shell.html`, `src/styles/*.css`, `src/game/*.js`, and `src/manifest.txt`.
- Generated: `Airbourne-Arena/index.html`.
- Generated mirror: `Airbourne-Arena/source/public/case-run.html`.
- Never hand-edit either generated file.
- The source split is concatenation, not an ES-module graph. Do not add `import` or `export` to the part files.
- `src/manifest.txt` is the load-order/dependency graph. Add parts next to their owning system and list every part exactly once.

The current canonical manifest contains 14 ordered style parts and 52 ordered game-script parts. Preserve the shared-scope and load-time ordering assumptions unless a separately approved migration replaces the build contract.

## Build and test gates

Run from `Airbourne-Arena/source`:

```bash
npm run build:game
node --test tests/game-html.test.mjs tests/game-build.test.mjs
```

Before shipping or opening a PR, also run:

```bash
bash scripts/build-game.sh --check
bash scripts/sync-game.sh --check
```

The tests enforce generated-file sync, complete manifest coverage, no module syntax, relative asset paths, dual-root asset presence, branding, controls, campaign/runtime invariants, and selected rendering behavior. Extend tests when adding a durable invariant; do not weaken an assertion merely to make a change pass.

## Asset contract

- Standalone asset root: `Airbourne-Arena/assets/`.
- Served mirror: `Airbourne-Arena/source/public/assets/`.
- Every runtime asset reference must remain relative.
- Every referenced asset must exist in both roots.
- Blender-authored runtime assets already include world LODs and a campaign story kit. Inspect and reuse naming/scale conventions before creating replacements.
- Dispose campaign/mission geometry, materials, and generated canvas textures when removed. Three.js does not free GPU resources merely because an object leaves the scene graph.

## Browser-first lane

The current shipped product is Three.js r128 plus browser-native HTML/CSS/JS. Improve and release this lane independently. A Unity project is a parallel port/prototype until it meets feature, performance, mobile, deployment, and regression parity; never replace the working browser game with an incomplete Unity build.

## Default measurement scenarios

Use comparable scripted or manually repeatable scenarios:

1. Cold load to controllable aircraft.
2. Arena match with eight aircraft and active weapons.
3. Dense authored-world flyover.
4. Campaign mission start/end repeated at least three times to expose leaks.
5. Phone portrait and landscape menus/touch flight.
6. Gamepad menu, hangar, and flight transitions.

Capture at least frame-time p50/p95, renderer calls/triangles/textures/geometries where available, JS heap or browser memory trend, transferred asset bytes, and visual/input regressions. Compare the same browser, viewport, quality mode, camera path, and warm-up.

## Starting asset budgets

Budgets are planning defaults, not universal laws. Tighten or relax them only with in-engine evidence.

| Asset | LOD0 | LOD1 | LOD2 | Typical texture ceiling |
|---|---:|---:|---:|---:|
| Player/hero fighter | 40k triangles | 15k | 5k | 2K per major PBR set |
| Repeated AI fighter | 20k | 8k | 2k | 1K–2K atlas |
| Large landmark | 60k visible section | 20k | 6k | 2K atlas |
| Small prop | 3k | 1k | 300 | 512–1K atlas |

Prefer shared materials, atlases, LODs, culling, and instancing for repeated objects. Measure decode time before choosing Draco; smaller transfer size can trade against slower low-end-device startup.

## Pull-request handoff

Every substantial PR should include:

- Player-facing change.
- Source files changed and generated outputs rebuilt.
- Test commands and results.
- Before/after metrics for optimization work.
- Desktop/mobile screenshots for visual work.
- Asset source/provenance and triangle/texture budgets for 3D work.
- Known risks and one-step rollback.
