# Cloud-Gap Explorer
![KP](assets/logo-mark.svg)

Built by Kanak Prabhakar

Measure how many AOI pixels are usable on both acquisition dates and inspect their spatial distribution offline.

![Demo: two Sentinel-2 scene-classification masks compared inside an AOI](assets/demo.gif)

The demo shows real output. Of the 8,836 AOI pixels, 678 (7.7%) are clear on both 18 and 28 January 2024. QGIS Raster Calculator gives exactly the same answer: 0 pixel disagreements.

## Features and architecture
Accept a WGS84 polygon and aligned GeoTIFFs. The loader supplies grid metadata, center-in-polygon membership and clear flags. A replacement loader can decode Resourcesat quality flags after validation against its product specification.

```mermaid
flowchart LR
 GeoTIFF --> Loader --> Intersection --> CSV_and_map
```

## Installation and usage
From the extracted project directory, run `python -m pip install -r requirements.txt` in a Python 3.11+ virtual environment. After setup the analysis runs offline.

```sh
python cloudgap.py sample/aoi.geojson comparison 2024-01-18=sample/2024-01-18.tif 2024-01-28=sample/2024-01-28.tif
python -m pytest -q 
python bench.py sample/aoi.geojson sample/2024-01-18.tif sample/2024-01-28.tif sample/qgis-reference.tif
```

## Benchmark protocol
In QGIS Raster Calculator build a 0/1 reference using ((A@1=4) OR (A@1=5) OR (A@1=6)) AND the same expression for B@1. Quote band names, choose A's CRS, extent and resolution. Export GeoTIFF. The benchmark treats reference nodata as unavailable and compares every AOI-center pixel. Runtime covers Python comparison only. Crop inputs to a shared footprint fully containing the AOI.

| Reference | AOI pixels | Clear in both | Pixel disagreements |
|---|---:|---:|---:|
| QGIS 3.44.14 Raster Calculator, 18 and 28 January 2024 | 8,836 | 678 | 0 |

## Limitations and roadmap
Coverage uses pixel counts. AOIs extending beyond the input footprint need clipping or explicit footprint testing. Large crops use RAM. Next add a validated Resourcesat loader.

## Resume line
Accomplished an offline two-date clear-sky coverage tool that matches QGIS Raster Calculator pixel for pixel (0 disagreements over 8,836 AOI pixels, 678 jointly clear) in about 0.03 s of comparison time, as measured by `bench.py` against an exported QGIS reference raster, by doing boolean Sentinel-2 SCL intersections on a shared grid with nodata kept in the denominator.

This is one AOI and one date pair, so the claim is "agrees with QGIS", not "faster than QGIS". The QGIS run time was not timed. To rebuild the reference use QGIS Python with `python qgis_reference.py sample/2024-01-18.tif sample/2024-01-28.tif reference.tif`. Open sample-report/map.html for all three date pairs. Source imagery and modifications are credited in sample/SOURCES.md.

## Credits
[Rasterio](https://rasterio.readthedocs.io/), [QGIS](https://qgis.org/), [NumPy](https://numpy.org/), [Pillow](https://python-pillow.org/), [pytest](https://pytest.org/).

## Presentation

1. I cropped aligned classification masks to a polygon in cloudgap.py.
2. I counted clear pixels on both dates and kept unavailable pixels in the denominator.
3. I exported the comparison to pairs.csv and embedded the spatial mask in map.html.
4. I used test_cloudgap.py to check nodata, duplicate dates and grid mismatches.
5. I compared against QGIS Raster Calculator with qgis_reference.py and bench.py.

**Main limitation.** The current loader expects aligned SCL grids and a polygon within both footprints.


See PRD.md, TRD.md and edge-cases.md for the design, and tests-output.txt / results.txt for the latest runs.
