"""Run with Blender Python after installing the official MPFB extension."""
from pathlib import Path
import json
import zipfile
from bl_ext.blender_org.mpfb.services.assetservice import AssetService
from bl_ext.blender_org.mpfb.services.locationservice import LocationService

root = Path(__file__).resolve().parents[1]
archive = root / 'tooling/downloads/makehuman_system_assets_cc0.zip'
error = AssetService.check_asset_pack_zip(str(archive))
if error:
    raise RuntimeError(error)
with zipfile.ZipFile(archive) as pack:
    pack.extractall(LocationService.get_user_data())
AssetService.update_all_asset_lists()
data = Path(LocationService.get_user_data())
report = {'data_directory': str(data), 'assets': [str(p.relative_to(data)) for p in data.rglob('*') if p.suffix in ('.mhclo', '.mhmat')]}
(root / 'tooling/mpfb-assets.json').write_text(json.dumps(report, indent=2))
print('MPFB_ASSETS_READY', len(report['assets']))
