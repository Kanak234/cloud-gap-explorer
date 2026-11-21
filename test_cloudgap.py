import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin
from cloudgap import compare, write

geo = {"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}


def test_raster(tmp_path):
    files = []
    for name, values in [("A", [[4, 0], [5, 6]]), ("B", [[4, 5], [9, 6]])]:
        path = tmp_path / (name + ".tif")
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            height=2,
            width=2,
            count=1,
            dtype="uint8",
            crs="EPSG:4326",
            transform=from_origin(0, 2, 1, 1),
            nodata=0,
        ) as ds:
            ds.write(np.array(values, dtype="uint8"), 1)
        files.append((name, path))
    assert next(compare(files, geo))[2:4] == (2, 4)
    write(files, geo, tmp_path / "out")
    assert "image/png" in (tmp_path / "out/map.html").read_text(encoding="utf8")


def test_duplicate_dates():
    with pytest.raises(ValueError):
        list(compare([("a", None), ("a", None)], geo))


def test_loader_grid_mismatch():
    class Loader:
        def load(self, path, geometry):
            mask = np.ones((2, 2), dtype=bool)
            return path, mask, mask

    with pytest.raises(ValueError, match="common grid"):
        list(compare([("a", "grid1"), ("b", "grid2")], geo, Loader()))
