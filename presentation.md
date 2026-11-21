# Presentation — Cloud-Gap Explorer

1. I cropped aligned classification masks to a polygon in cloudgap.py.
2. I counted clear pixels on both dates and kept unavailable pixels in the denominator.
3. I exported the comparison to pairs.csv and embedded the spatial mask in map.html.
4. I used test_cloudgap.py to check nodata, duplicate dates and grid mismatches.
5. I compared against QGIS Raster Calculator with qgis_reference.py and bench.py.

**Main limitation.** The current loader expects aligned SCL grids and a polygon within both footprints.
