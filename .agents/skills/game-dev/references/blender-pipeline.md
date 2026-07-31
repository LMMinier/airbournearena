# Blender game-asset pipeline

## Deliverables

A production asset is a set, not a screenshot:

- Editable `.blend` source.
- Runtime `.glb`/`.gltf` or approved engine-native export.
- Texture source and runtime textures.
- LODs and collision when required.
- Rig/animations when required.
- Asset brief, budgets, provenance/license, and runtime screenshots.

Use generated raster images as concept/reference material, not proof of a mesh.

## Scene conventions

- Work in meters unless the target project proves another convention.
- Establish the runtime forward/up convention with a minimal round-trip test. Blender is Z-up; glTF performs the standard coordinate conversion. Do not add unexplained corrective rotations to every asset.
- Apply scale before bevel widths, physics, LOD generation, and export. Avoid negative scale on final export objects.
- Put origins/pivots where gameplay rotates, attaches, aims, or places the asset.
- Keep generated content under a clearly named script-owned collection.
- Use deterministic names such as `fighter__body__lod0`, `fighter__body__lod1`, `fighter__collision`, and `fighter__socket_muzzle`.

## Geometry

- Inspect evaluated modifier output, not only the base cage.
- Remove duplicate/loose vertices, zero-area faces, unintended internal geometry, and degenerate triangles.
- Resolve inverted normals and use intentional smooth/hard edges. Do not hide broken topology with indiscriminate smoothing.
- Keep deformation topology clean around joints; static environment topology may optimize more aggressively.
- Triangulate deterministically at export or with an export modifier when exact runtime topology matters.
- Build collision separately from render detail. Never use a hero render mesh as default collision without evidence.
- Create LODs by preserving silhouette, control surfaces, emissive landmarks, and gameplay-readable shapes before small surface detail.

## UVs, materials, and textures

- Every textured render mesh needs a valid UV set with intended texel density and padding.
- Prefer a small, shared PBR material vocabulary: base color, metallic, roughness, normal, emissive, and occlusion only where used.
- Bake high-frequency geometry into normal/ambient-occlusion maps when it is cheaper and visually stable.
- Avoid unbounded procedural/material node graphs that cannot export to glTF. Bake unsupported effects.
- Pack channels only when the runtime shader and color-space handling are explicitly matched.
- Use sRGB for color textures and non-color data for normal/metallic/roughness/occlusion maps.

## Rigging and animation

- Name bones and actions deterministically.
- Keep a single authoritative armature and remove unused deform bones from export.
- Normalize weights and inspect maximum influences supported by the target runtime.
- Put repeatable clips in Actions/NLA according to the selected glTF animation export mode.
- Test first/last-frame continuity for loops and root-motion policy in engine.

## Export and validation

Prefer glTF 2.0/GLB for the browser lane. Export selected objects/collections only, apply intended modifiers, include required normals/tangents/UVs/materials/animations, and avoid exporting cameras/lights/helpers unintentionally.

Run:

```bash
blender -b path/to/asset.blend --python scripts/audit_blender_scene.py -- --json /tmp/asset-audit.json
python scripts/audit_glb.py path/to/asset.glb
```

Then load the exact exported file in the actual game. Check scale, axis, pivot, material color space, animation clips, LOD switching, collision, draw calls, triangles, texture count, memory trend, and appearance under runtime lighting.

## Sources

- Blender 5.2 LTS glTF exporter: https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html
- Apply transforms: https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html
- Texture baking: https://docs.blender.org/manual/en/latest/render/cycles/baking.html
- Normals: https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html
- Actions: https://docs.blender.org/manual/en/latest/animation/actions.html
