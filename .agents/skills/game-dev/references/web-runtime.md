# Browser, Three.js, and mobile runtime

## Compatibility first

Determine the exact Three.js revision and browser contract before copying current examples. Airbourne Arena uses r128 and a non-module, `file://`-compatible build; modern addon import paths and APIs may not apply without an explicit engine upgrade.

Upgrade Three.js only as a dedicated change with loader, material/color-management, shader, asset, browser, performance, and visual regression checks.

## Measure frame behavior

- Profile representative gameplay, not an empty scene or editor preview.
- Warm up shaders/assets before the measured window unless measuring cold start.
- Record p50 and p95 frame time; averages hide stutter.
- Separate CPU and GPU hypotheses when tooling permits.
- Sample `renderer.info.render.calls`, triangles, points, lines, and `renderer.info.memory.geometries/textures` on the same camera path.
- Repeat mission/load transitions to find monotonic resource growth.
- Profile at target device pixel ratios. Cap pixel ratio on constrained devices when the visual tradeoff is acceptable.

## Rendering priorities

1. Remove leaks and unnecessary per-frame allocation.
2. Cull work outside the camera or active gameplay region.
3. Reuse geometry, material, loader, and texture instances.
4. Instance repeated meshes when geometry/material and gameplay constraints permit.
5. Add LODs with stable silhouettes and conservative switch distances.
6. Reduce transparent overdraw, shadow casters, dynamic lights, and post-processing on lower tiers.
7. Compress meshes/textures only after measuring transfer, decode, GPU-memory, and quality costs.

Removing an object from a scene is not disposal. Explicitly dispose owned geometries, materials, textures, render targets, loaders/generators with disposable resources, audio nodes, and event listeners. Do not dispose shared assets while other objects still use them.

## Asset delivery

- Prefer glTF/GLB for runtime meshes and animations.
- Draco can reduce geometry transfer size but adds decoder/download/CPU cost; reuse one decoder instance.
- KTX2/Basis can reduce GPU texture memory and transfer size but requires compatible loaders/transcoders and browser testing.
- Preserve mipmaps for 3D surfaces; avoid oversized UI textures and alpha channels that are not used.
- Use content hashes or versioned names when caching would otherwise serve stale art.

## Mobile and accessibility

- Test portrait and landscape, safe-area insets, browser chrome changes, and software keyboard/visual viewport behavior.
- Keep critical touch targets at least roughly 44 CSS pixels and separated enough to prevent accidental activation.
- Do not require hover. Pair icons with accessible names.
- Respect `prefers-reduced-motion`; avoid camera shake, flashes, and parallax when reduced motion is active.
- Ensure HUD scaling does not overlap controls or hide objectives.
- Test touch cancellation, multi-touch, pointer capture loss, orientation change, pause/resume, and interrupted audio context.
- Maintain keyboard and gamepad paths when changing menus.
- Color must not be the only carrier of team, warning, or target state.

## Web QA matrix

At minimum, test:

- Chromium desktop and a mobile Chromium-class browser.
- WebKit/iPhone-class behavior when release scope includes iOS.
- Mouse/keyboard, touch, and standard gamepad.
- Fresh storage, existing save, corrupted save, and storage unavailable.
- Cold cache and warm cache.
- Reduced motion, color-blind palette, smallest/largest HUD scale.
- Context loss/backgrounding and return to play.

## Sources

- Three.js `WebGLRenderer.info`: https://threejs.org/docs/
- Three.js `InstancedMesh`: https://threejs.org/docs/pages/InstancedMesh.html
- Three.js `GLTFLoader`: https://threejs.org/docs/pages/GLTFLoader.html
- Three.js `DRACOLoader`: https://threejs.org/docs/pages/DRACOLoader.html
- Three.js `KTX2Loader`: https://threejs.org/docs/pages/KTX2Loader.html
- Three.js texture disposal: https://threejs.org/docs/pages/Texture.html
