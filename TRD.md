# Technical design
Accept a WGS84 polygon and aligned GeoTIFFs. The loader supplies grid metadata, center-in-polygon membership and clear flags. A replacement loader can decode Resourcesat quality flags after validation against its product specification.

Coverage uses pixel counts. AOIs extending beyond the input footprint need clipping or explicit footprint testing. Large crops use RAM. Next add a validated Resourcesat loader.
