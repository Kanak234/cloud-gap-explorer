"""Prepare a fixed 96x96-pixel crop of two public Sentinel-2 L2A acquisitions."""

import argparse
import json
from pathlib import Path
import rasterio
from rasterio.windows import Window, bounds, transform
from rasterio.warp import transform_geom


def main():
    p = argparse.ArgumentParser()
    p.add_argument("first", type=Path)
    p.add_argument("second", type=Path)
    p.add_argument("destination", type=Path)
    p.add_argument("--third", type=Path, help="Optional 28 January scene")
    args = p.parse_args()
    args.destination.mkdir(exist_ok=True)
    sources = [("2024-01-08", args.first), ("2024-01-18", args.second)]
    if args.third:
        sources.append(("2024-01-28", args.third))
    for date, path in sources:
        with rasterio.open(path) as source:
            window = Window(2700, 2700, 96, 96)
            crop = source.read(1, window=window)
            affine = transform(window, source.transform)
            with rasterio.open(
                args.destination / (date + ".tif"),
                "w",
                driver="GTiff",
                width=96,
                height=96,
                crs=source.crs,
                transform=affine,
                count=1,
                dtype=crop.dtype,
                nodata=0,
                compress="deflate",
            ) as out:
                out.write(crop, 1)
            # Inset the polygon so rounding during the CRS round-trip stays within the crop.
            x0, y0, x1, y1 = bounds(Window(2701, 2701, 94, 94), source.transform)
            ring = [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]
            geo = transform_geom(
                source.crs, "EPSG:4326", {"type": "Polygon", "coordinates": [ring]}
            )
            (args.destination / "aoi.geojson").write_text(
                json.dumps(geo), encoding="utf8"
            )


if __name__ == "__main__":
    main()
