# Sentinel-2 sample attribution
Contains modified Copernicus Sentinel data (2024), distributed in the Element 84 Earth Search Sentinel COGs archive. The supplied GeoTIFFs are cropped classification masks. Each pixel remains in the original grid and retains the original SCL class.

- [8 January source](https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/43/P/GN/2024/1/S2A_43PGN_20240108_0_L2A/SCL.tif)
- [18 January source](https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/43/P/GN/2024/1/S2A_43PGN_20240118_0_L2A/SCL.tif)
- [28 January source](https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/43/P/GN/2024/1/S2A_43PGN_20240128_0_L2A/SCL.tif)

Use prepare_sample.py to reproduce the 96-by-96 crops from the two required source files. The polygon selects an inset 94-by-94 region. Timing excludes download.
