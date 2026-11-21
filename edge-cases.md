# Tested edge cases
- nodata pixels (kept in the denominator, never clear)
- cloudy pixels (SCL classes outside 4/5/6)
- date collisions (duplicate dates rejected)
- grid mismatch (rejected with "common grid" message)
- AOI extending outside the raster footprint (rejected)
- embedded offline image (map.html contains a data: PNG)
