---
name: game-dev
description: End-to-end game production for browser, Three.js/WebGL, Blender, and Unity projects. Use when creating or improving gameplay, controls, mobile layout, UI/HUD, rendering, performance, game assets, 3D meshes, animation, levels, build pipelines, tests, release readiness, or a measured production backlog. Tailored to Airbourne Arena when that repository is in scope. Do not use for a standalone image with no game integration, general prose about games, or unrelated software work.
---

# Game development production house

Own the requested game-development outcome from inspection through verified handoff. Treat design, engineering, art, performance, accessibility, and release operations as one production system.

## Start every task

1. Read applicable `AGENTS.md` files and repository guidance.
2. Inspect the current source of truth, working-tree state, build instructions, tests, asset layout, target platforms, and deployed runtime before proposing a rewrite.
3. Classify the task into one or more lanes:
   - **Browser runtime**: JavaScript/TypeScript, Three.js/WebGL, HTML/CSS, PWA.
   - **Blender asset**: modeling, UVs, materials, rigging, animation, LODs, collision, export.
   - **Unity lane**: Unity project, C#, URP, input, Web/desktop/mobile builds.
   - **Experience design**: game loop, UX, HUD, menus, accessibility, narrative, balancing.
   - **Release**: profiling, compatibility, CI, packaging, store/site readiness.
4. State the player-facing outcome and a measurable definition of done before editing.
5. Capture a baseline for anything described as faster, smaller, smoother, clearer, or optimized. Never claim an improvement without before/after evidence.

If Airbourne Arena is in scope, read `references/airbourne-arena.md` completely before acting.

## Route to the relevant references

- Browser, Three.js, mobile layout, or Web performance: read `references/web-runtime.md`.
- Blender, mesh, texture, rig, animation, or `.glb`/`.gltf`: read `references/blender-pipeline.md`.
- Unity, C#, URP, or Unity Web builds: read `references/unity-lane.md`.
- Release, optimization, QA, or “ready to ship”: read `references/release-gates.md`.

Read only the references required for the selected lanes, but read each selected reference completely.

## Production decision rules

- Prefer one bounded, high-impact vertical slice over a broad unverified rewrite.
- Preserve working gameplay and repository contracts. Add a parallel migration lane when changing engines or build systems.
- Separate observed facts, measurements, hypotheses, and aesthetic judgment.
- Fix correctness and broken player flows before polish; fix frame-time spikes and leaks before raising visual complexity.
- Reuse existing design language, controls, systems, shaders, materials, and story canon before creating parallel systems.
- Do not add a dependency merely because it is fashionable. Record its runtime cost, license, compatibility, and removal plan.
- Do not edit generated artifacts directly. Find and edit their source, then rebuild.
- Do not push directly to a protected/default branch or deploy unless the user explicitly authorizes it.
- Preserve unrelated user changes in dirty worktrees.
- Stop and ask when a choice changes canon, monetization, licensing, target platforms, account systems, or irreversible release state.

## Visual and asset workflow

When original raster art would materially improve the game, invoke the available `imagegen` skill and use the image model for concept sheets, orthographic turnarounds, texture ideas, decals, UI, key art, or skybox references.

Never describe a generated image as a mesh or production-ready 3D asset. A 3D deliverable requires geometry, topology, scale, pivots, normals, UVs, materials, LODs, collision as needed, export, runtime integration, and visual/performance validation.

For Blender assets:

1. Define the asset brief and runtime budgets first.
2. Keep the editable `.blend` source.
3. Produce deterministic export settings or an export script.
4. Audit the scene with `scripts/audit_blender_scene.py` when Blender is available.
5. Audit final `.glb` files with `scripts/audit_glb.py`.
6. Wire the exact exported asset into the runtime; do not stop at an unattached render.
7. Capture in-engine screenshots from representative gameplay distances.

Record provenance and license for every external or generated asset. Do not imitate a protected franchise, artist, logo, or vehicle design too closely.

## Implementation loop

1. Reproduce or baseline the current behavior.
2. Identify the narrowest source files and systems that own it.
3. Write or update a regression test when the behavior can be checked deterministically.
4. Implement the smallest coherent change.
5. Rebuild generated outputs through the repository’s own scripts.
6. Run targeted tests, then the full relevant gate.
7. Perform visual QA for any visible change. Inspect desktop and mobile/touch layouts when supported.
8. Measure the same metric and scenario used for the baseline.
9. Review the diff for generated-file drift, dead assets, accidental branding/canon changes, secrets, and unrelated edits.
10. Hand off the result with evidence, remaining risks, and the next highest-impact task.

If a required editor or runtime is unavailable, do not fake verification. Produce deterministic source/scripts and label which checks remain unexecuted.

## Definition of done

A game-development task is done only when all applicable statements are true:

- The player-facing outcome exists in the actual runtime, not just a mockup.
- Source files, generated outputs, and asset copies are synchronized.
- Tests/builds pass, or the exact blocker and unexecuted command are reported.
- Visible changes were inspected at target viewport/device classes.
- Performance claims include comparable before/after measurements.
- New assets meet agreed budgets and have source, provenance, and runtime wiring.
- Controls remain usable with the supported input methods.
- Save data and canon remain compatible or have an explicit migration.
- The handoff names modified files, evidence, risks, and rollback path.

## Continuous production mode

For recurring work, maintain a compact production log with: current baseline, completed task IDs, measurements, blockers, next candidates, and links to branches/PRs or artifacts. Choose one task per run. Do not repeat completed or blocked work without new evidence. Never let recurring automation merge or deploy autonomously.
