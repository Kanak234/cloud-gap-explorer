# PRD — Cloud-Gap Explorer

## Problem
To compare two satellite dates over a field, district or project site (crop change, flood extent, construction), you need pixels that are cloud-free on *both* dates. Checking the scene-level cloud percentage is misleading, because a scene can be 5% cloudy overall and 90% cloudy over your area. Doing it properly in QGIS is a multi-step Raster Calculator job for every pair of dates.

## Users
- **Primary:** a student or GIS analyst with a polygon (GeoJSON) and a few Sentinel-2 L2A scene-classification (SCL) rasters, working offline.

## Goals
1. For every pair of dates, report how many AOI pixels are clear on both dates, and what fraction that is.
2. Show *where* those pixels are, in one portable HTML file.
3. Match a QGIS Raster Calculator result exactly on the same inputs.

## Non-goals
- Downloading imagery (the user supplies the rasters).
- Resampling or reprojecting between grids. Mismatched grids are refused rather than silently resampled.
- Area in km² (counts are in pixels for now).

## Features
| Feature | Behaviour |
|---|---|
| Input | WGS84 GeoJSON polygon + `DATE=path.tif` masks on one grid |
| Clear classes | SCL 4 (vegetation), 5 (bare soil), 6 (water) |
| Denominator | every pixel whose centre is inside the AOI, nodata included |
| Output | `pairs.csv` (first, second, clear_pixels, aoi_pixels, clear_fraction) + `map.html` with an embedded PNG per pair |
| Pluggable loader | `SentinelSCL` can be swapped for another product (e.g. Resourcesat) after validation |

## Acceptance criteria
- `python -m pytest -q` passes.
- `bench.py` on the sample gives `disagreeing_pixels: 0` against `sample/qgis-reference.tif`.
- Duplicate dates, grid mismatch, an AOI outside the footprint, or an AOI with no pixel centres stop the run with a clear error.
