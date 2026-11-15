# Final rendered check

All 27 runtime checks passed with Will's colored materials and the arena fill
light. Movement, jump/landing, attack timing, damage, guard, knockout and reset
work with the replacement visual. These checks exercise the existing prototype
combat; authored punch animations and facial animation are not implemented.

| Same arena, same camera | Mean FPS | Mean frame time | 95th-percentile frame time | Frames sampled |
| --- | ---: | ---: | ---: | ---: |
| Will custom character | 57.0 | 17.54 ms | 32 ms | 457 |
| Original mannequin | 59.9 | 16.70 ms | 31 ms | 480 |

Measured in rendered Unreal 5.8.3 editor PIE on the MX150 2 GB, using DX11, low
scalability and 70% screen percentage. The captured viewport is 1018 x 556.
Each sample runs for at least eight seconds after warmup. Samples use the
editor's Slate tick wall times; they include editor overhead. `t.MaxFPS` was
temporarily set to zero and restored to 60. Screenshot capture happens after
sampling. These figures describe this small preview scene, not a packaged-game
benchmark or a guarantee for more fighters/effects.

NVIDIA's total GPU-memory-used counter read 456 MiB during both samples, including
the editor and resident assets from both comparison models. This is not the
isolated memory cost of Will. No video-memory-exhausted warning appeared in the
final run. The detailed source is preserved; the runtime character uses 96,376
triangles and three 2048px skin maps.

`arena-runtime.png` and `close-up-runtime.png` are actual final Unreal captures.
`full-body-review.png` is a separate Blender review render. The skin/outfit still
need art review; there is no approved final likeness or facial rig.
