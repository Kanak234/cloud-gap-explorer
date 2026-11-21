"""Compare aligned categorical satellite masks inside a GeoJSON polygon."""

from pathlib import Path
import argparse
import csv
import html
import itertools
import json
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.features import bounds, geometry_mask
from rasterio.warp import transform_geom


class SentinelSCL:
    """A loader returns a grid signature, AOI membership and usable pixel masks."""

    def load(self, path, geometry):
        with rasterio.open(path) as src:
            projected = transform_geom("EPSG:4326", src.crs, geometry)
            west, south, east, north = bounds(projected)
            if (
                west < src.bounds.left
                or east > src.bounds.right
                or south < src.bounds.bottom
                or north > src.bounds.top
            ):
                raise ValueError("AOI extends outside the source footprint")
            data, affine = mask(src, [projected], crop=True, filled=False, indexes=1)
            inside = geometry_mask([projected], data.shape, affine, invert=True)
            # Keep nodata inside the denominator. Use conservative clear classes only.
            clear = inside & ~np.ma.getmaskarray(data) & np.isin(data.data, [4, 5, 6])
            return (src.crs, affine, data.shape), inside, clear


def compare(items, geometry, loader=None):
    loader = loader or SentinelSCL()
    if len(items) < 2 or len(dict(items)) != len(items):
        raise ValueError("Provide at least two uniquely dated masks")
    masks = [(date, *loader.load(path, geometry)) for date, path in items]
    for (a, grid, inside, x), (b, other, region, y) in itertools.combinations(masks, 2):
        if grid != other or not np.array_equal(inside, region):
            raise ValueError(
                "Resample categorically to one common grid before analysis"
            )
        count = int(inside.sum())
        if not count:
            raise ValueError("AOI contains no pixel centers")
        shared = x & y
        yield a, b, int(shared.sum()), count, shared


def write(items, geometry, dest):
    import base64
    from io import BytesIO
    from PIL import Image

    pairs = list(compare(items, geometry))
    dest.mkdir(exist_ok=False)
    pages = [
        '<meta charset="utf-8"><h1>Pairwise clear coverage</h1><p>Green: jointly clear. Gray: other pixels in the cropped extent. Images follow the source raster grid.</p>'
    ]
    with (dest / "pairs.csv").open("w", newline="") as stream:
        out = csv.writer(stream)
        out.writerow(
            ["first", "second", "clear_pixels", "aoi_pixels", "clear_fraction"]
        )
        for a, b, n, total, pixels in pairs:
            out.writerow([a, b, n, total, n / total])
            # Embed the actual spatial intersection so the report remains portable offline.
            image = Image.fromarray(
                np.where(pixels[:, :, None], [35, 151, 101], [219, 221, 223]).astype(
                    "uint8"
                )
            )
            data = BytesIO()
            image.save(data, format="PNG")
            encoded = base64.b64encode(data.getvalue()).decode()
            pages.append(
                f'<h2>{html.escape(a)} / {html.escape(b)} · {n/total:.1%}</h2><img alt="Clear overlap map" src="data:image/png;base64,{encoded}">'
            )
    (dest / "map.html").write_text("".join(pages), encoding="utf8")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("aoi", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("dated_masks", nargs="+", help="DATE=path.tif")
    args = p.parse_args()
    geo = json.loads(args.aoi.read_text())
    write(
        [item.split("=", 1) for item in args.dated_masks],
        geo.get("geometry", geo),
        args.output,
    )
