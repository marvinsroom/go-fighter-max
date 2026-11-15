# Shared combat reviews

Rimuru, Cid and Jinwoo use `scripts/fighter_review.py` with one shell (`fighter-review.html`), stylesheet (`fighter-review.css`) and player (`fighter-review.js`). Data is embedded with each page so the menu and capture revision stay together. Each page starts with character navigation, native captures and ultimate shortcuts, then controls and character-specific details.

The current packagers all call this renderer:

- `package-rimuru.py`
- `package-cid-illustrated.py --review-only`
- `package-jinwoo-current.py`

Rimuru and Cid supply their generated content and refresh their `*-review-content.html` snapshots. Jinwoo's editable character content lives in `jinwoo-review-content.html`. Run `scripts/fighter_review.py` to refresh all three layouts using existing capture data and content snapshots. It also keeps Rimuru's v3/v4 aliases synchronized and generates Cid's proportion-audit page.

Run `scripts/verify-fighter-reviews.cjs` with Node to check all capture paths, category/clip selection, ultimate shortcuts, image-load timing, playback, errors/recovery, artwork controls and shared CSS/JavaScript. Native combat evidence remains owned by each character's existing packager and validators.
