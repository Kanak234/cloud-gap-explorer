# TRD — Cloud-Gap Explorer

## Stack
Python 3.11+, Rasterio (GDAL) for reading and masking, NumPy for boolean maths, Pillow for the PNG embedded in `map.html`. A QGIS Python script (`qgis_reference.py`) builds the independent reference.

## Data flow
1. `SentinelSCL.load(path, geometry)`:
   - Reproject the WGS84 polygon to the raster CRS (`transform_geom`).
   - Refuse if its bounds leave the raster footprint.
   - `rasterio.mask.mask(crop=True, filled=False)` gives a masked array. `geometry_mask(invert=True)` gives centre-in-polygon membership.
   - `clear = inside & ~nodata & isin(SCL, [4, 5, 6])`.
   - Return the grid signature `(crs, affine, shape)`, `inside` and `clear`.
2. `compare(items, geometry, loader)`:
   - Require ≥ 2 unique dates.
   - For each pair, require identical grid signatures and AOI masks.
   - Yield `(a, b, clear-in-both count, AOI count, boolean map)`.
3. `write()`: CSV row per pair, plus a green/grey PNG of the joint-clear map, base64-embedded so the HTML works offline.
4. `bench.py`: compares the tool's boolean map with the QGIS 0/1 raster pixel by pixel, treating reference nodata as unavailable.

## Key decisions
- **Nodata stays in the denominator.** Missing data is not "clear", and dropping it would inflate coverage.
- **Refuse, don't resample.** Categorical classes must not be interpolated, so the user aligns grids first, deliberately.
- **Conservative clear classes.** Cloud shadow (3), thin cirrus (10) and snow (11) count as not usable.

## Limits and roadmap
Pixel counts, not area. One CRS per run. The AOI must sit inside both footprints. Next: a validated Resourcesat loader, and area in hectares.
