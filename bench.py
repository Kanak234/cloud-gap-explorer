"""Compare one pair against an aligned binary QGIS reference raster."""

import argparse, json, time
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom
from cloudgap import compare, SentinelSCL

p = argparse.ArgumentParser()
for arg in ("aoi", "first", "second", "reference"):
    p.add_argument(arg)
args = p.parse_args()
with open(args.aoi) as f:
    geo = json.load(f)
geo = geo.get("geometry", geo)
start = time.perf_counter()
_, _, n, total, actual = next(compare([("A", args.first), ("B", args.second)], geo))
seconds = time.perf_counter() - start
grid, inside, _ = SentinelSCL().load(args.first, geo)
with rasterio.open(args.reference) as src:
    ref, aff = mask(
        src,
        [transform_geom("EPSG:4326", src.crs, geo)],
        crop=True,
        indexes=1,
        filled=False,
    )
    if (src.crs, aff, ref.shape) != grid:
        raise ValueError("QGIS reference grid differs")
    expected = ref.filled(0) == 1
print(
    dict(
        disagreeing_pixels=int(((actual != expected) & inside).sum()),
        aoi_pixels=total,
        clear_pixels=n,
        seconds=seconds,
    )
)
