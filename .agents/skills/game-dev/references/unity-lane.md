# Unity production lane

## Relationship to an existing game

For Airbourne Arena, Unity is a parallel port lane, not an automatic replacement for the working Three.js build. Establish parity gates and keep the browser release shippable while the port develops.

Create an explicit mapping for:

- Flight state and physics assumptions.
- Input actions for keyboard/mouse, gamepad, and touch.
- Arena objectives, teams, AI, weapons, mission state, saves, and campaign flags.
- Asset scale, pivots, sockets, LODs, collision, and material semantics.
- HUD/menu/accessibility behavior.
- Deterministic test scenarios and expected outcomes.

Do not mechanically translate shared-scope JavaScript into monolithic C#. Port behavior into testable Unity systems.

## Project baseline

- Prefer the current supported Unity 6 LTS patch for a new production project unless a package/platform constraint requires another version.
- Use URP for a cross-platform stylized/real-time project unless measured requirements justify another pipeline.
- Commit `ProjectSettings`, `Packages`, and `Assets`; ignore `Library`, `Temp`, `Logs`, and generated build directories.
- Pin package versions and record Unity Editor version in `ProjectVersion.txt`.
- Prefer Editor scripts/import presets over manual repeated inspector work.

## Runtime architecture

- Separate simulation state from presentation and input collection.
- Use the Input System with explicit action maps and rebinding where supported.
- Pool high-frequency objects such as bullets, effects, markers, and repeated enemies.
- Avoid per-frame allocations and repeated scene searches in hot paths.
- Use ScriptableObjects for stable authored data, not mutable global runtime state.
- Version save data and test upgrade/failure behavior.
- Make quality tiers explicit rather than scattering device checks through gameplay code.

## URP and performance

- Profile a built player on target hardware; Editor measurements include Editor overhead and can misrepresent texture memory.
- Reduce unused URP features and shader variants.
- Minimize cameras, transparent overdraw, shadow distance/cascades, additional shadowed lights, post-processing, and high MSAA on constrained tiers.
- Use SRP Batcher/GPU instancing when shaders and object patterns support them.
- Remove unused packages, resources, scenes, shaders, and variants from release builds.
- Use LOD groups, occlusion/frustum culling, compressed textures, mip streaming where appropriate, and conservative Web memory settings.

## Unity Web lane

- Treat build size, startup time, memory, browser compatibility, input, and server headers as first-class requirements.
- Use Brotli only when the host serves the required content-encoding headers; otherwise choose a compatible compression/decompression fallback.
- Create separate Web build profiles for desktop and mobile texture/quality assumptions when necessary.
- Test the deployed build, not only `Build And Run`.
- Verify browser storage/save behavior, audio unlock, backgrounding, fullscreen/pointer lock, touch, and WebGL context recovery.

## Automated gates

When Unity is available, prefer batch-mode edit/play tests and deterministic build scripts. Example shape (replace the Editor path and method with project-owned values):

```bash
Unity -batchmode -nographics -quit -projectPath unity/AirbourneArena \
  -runTests -testPlatform EditMode -testResults artifacts/editmode.xml
Unity -batchmode -nographics -quit -projectPath unity/AirbourneArena \
  -executeMethod BuildAutomation.BuildWeb
```

Do not claim these passed unless their process exited successfully and expected result/build artifacts exist. Unity licensing and platform modules are legitimate CI blockers; report them exactly.

## Sources

- Unity Web optimization: https://docs.unity3d.com/6000.0/Documentation/Manual/web-optimization.html
- Mobile Web optimization: https://docs.unity3d.com/6000.1/Documentation/Manual/web-optimization-mobile.html
- Web texture compression: https://docs.unity3d.com/6000.0/Documentation/Manual/webgl-texture-compression.html
- URP performance: https://docs.unity3d.com/6000.0/Documentation/Manual/urp/configure-for-better-performance.html
- URP shader stripping: https://docs.unity3d.com/6000.0/Documentation/Manual/urp/shader-stripping.html
- Memory Profiler: https://docs.unity3d.com/6000.0/Documentation/Manual/com.unity.memoryprofiler.html
- Target-device profiling: https://docs.unity3d.com/6000.0/Documentation/Manual/profiling-target-device.html
