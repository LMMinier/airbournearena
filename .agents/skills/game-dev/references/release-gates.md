# Game release gates

Apply only the gates relevant to the target platform, but do not call a build release-ready while a required gate is untested.

## P0: integrity and blockers

- Repository source and generated artifacts are synchronized.
- Clean install/build/test succeeds from documented commands.
- No secrets, private credentials, unlicensed assets, broken links, or missing runtime files.
- No crash, soft lock, corrupted save, unrecoverable input loss, or deployment failure in the release path.
- Default branch remains recoverable; release/deploy actions are intentional and auditable.

## P1: player journey

- New player can launch, understand the immediate objective, enter gameplay, pause, configure controls, finish/fail, retry, and return to menus.
- Existing save loads; malformed/old save fails safely or migrates.
- Keyboard/mouse, touch, and gamepad work wherever the product claims support.
- Menus do not trap focus or require hover-only interaction.
- Loading and error states tell the player what happened.

## P1: performance

- Define target devices and frame-time budgets before declaring success.
- Capture comparable p50/p95 frame time and memory/resource trend in representative worst-case scenes.
- Repeat load/unload or mission transitions to expose leaks.
- Measure cold/warm transfer and time-to-interactive for Web builds.
- Record asset, bundle, shader, draw-call, triangle, and texture regressions relevant to the change.
- A prettier build that misses the agreed performance tier is not an unconditional upgrade; expose it as a quality tier or revise it.

## P1: visual and UX

- Inspect actual runtime screenshots/video at intended gameplay distance.
- Test supported aspect ratios, safe areas, HUD scales, color modes, reduced motion, and text overflow.
- Check readability over bright/dark/busy scenes and during damage/effects.
- Verify LOD transitions, z-fighting, clipping, normals, material color space, and missing-texture behavior.

## P1: content and systems

- Objectives can be completed and failed intentionally.
- AI, weapons, scores, rewards, upgrades, and difficulty changes have bounded values and regression coverage where practical.
- Story/canon changes match the authoritative design document.
- Save-affecting changes carry a version/migration decision.

## P2: release operations

- Version, changelog/release notes, licenses/credits, privacy/network disclosures, and support/contact path are correct for the destination.
- Deployment headers, caching, compression, MIME types, PWA manifest/icons, and offline claims are verified on the real host.
- Rollback is documented and tested enough to be credible.
- Monitoring captures build/deploy failure and material client errors without collecting unnecessary personal data.

## Evidence package

For every release candidate, retain:

- Commit/ref and build identifier.
- Commands and machine/runtime versions.
- Test results.
- Performance table with scenario/device/browser.
- Representative screenshots.
- Asset/license changes.
- Known issues, severity, owner, and decision.
- Rollback instruction.
