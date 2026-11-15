# TRELLIS.2 cel-shaded Will test

User requested using Hugging Face models to improve the rejected Will asset.
Tested the official Microsoft Space: https://huggingface.co/spaces/microsoft/TRELLIS.2
Availability check confirmed RUNNING and the public API responded. TencentARC's
Pixal3D was also running; VAST-AI CharacterGen reported RUNTIME_ERROR. These are
point-in-time checks, not guarantees of future availability or free capacity.

`will-cel-apose-input-v1.png` is a new isolated RGBA reference generated with the
built-in imagegen tool from `concepts/will-cel-design-target-v1.png`. Its exact
prompt is saved beside it. This is an input image, not a 3D mesh.

Sent only that isolated character image to Microsoft TRELLIS.2, using its public
unauthenticated API. No project files, credentials, payments or accounts were
used. Settings: 1024 generation, seed 2718; requested GLB 100k faces / 2048 texture.

**Generation produced a real 3D preview, but GLB extraction was refused with a
ZeroGPU quota error. NO GLB has been downloaded.** The error reported a 120-second
request versus 156 seconds remaining and recommended authentication or trying
again in about 24 hours. Preserve that exact service error in
`generation-result.json`; do not infer the unusual numeric comparison means the
export should have been accepted. Do not automatically retry or rotate identities.

`generated-preview.html` and the 48 `preview-mode*-view*.jpg` images are real
service-rendered generated geometry, including normal/clay/basecolor views.
They are not in-game captures, downloadable geometry or evidence of rigging.
Mode 2 view 4 is the front basecolor view; mode 2 view 3 is three-quarter.
Visual inspection: outfit silhouette is coherent and the head/hair are stylized,
but the face loses Will's distinctive proportions and must not be called approved
or a solved likeness. Shadows/colors in the generated texture are not a finished
Guilty Gear-like Unreal toon shader. No game assets were changed.

Opened the official Space in the browser and selected the input image in Explorer.
For a signed-in free-account attempt, upload that input, Generate, then Extract
GLB and Download GLB. Free quota may still apply; no paid upgrade is authorized.
The Python scripts are prepared for generation and subsequent mesh inspection,
but `inspect-will-trellis.py` must only run after a real GLB exists.

## Verified-account follow-up

User confirmed account verification. Used the existing signed-in Edge session
through Windows UI Automation, without reading cookies, passwords or tokens.
Uploaded the exact prepared reference; visually confirmed it on TRELLIS.2.
Both 1024 and a smaller 512 generation returned generic `Error` in the preview.
No explanatory quota/server message was exposed in visible labels or hover.
Do not claim the browser failures are proven quota errors or that export succeeded.
Original Microsoft TRELLIS metadata separately reported CONFIG_ERROR, so it was
not attempted. Pixal3D source was inspected but no image sent there: its export
requests a 240-second GPU allocation and free-account feasibility is unverified.
No paid upgrades, new accounts, API credentials or Unreal asset changes.
Browser remains on TRELLIS.2 with the reference loaded; no new GLB exists.

UI scripts: `inspect-huggingface-window.ps1` scopes screenshot/visible-label reads
to the HF/TRELLIS browser. UIA button invocation can work without foreground;
file upload used guarded keyboard entry into that browser's foreground Open
dialog because its filename field was not exposed by UIA. `use-huggingface-control.ps1`
has a filename-field lookup that fails on this dialog; do not repeatedly invoke
Upload while the existing dialog is open. Never type without checking foreground.
