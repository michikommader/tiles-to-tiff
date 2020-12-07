# tiles-to-tiff
Python script for converting XYZ raster tiles for slippy maps to a georeferenced TIFF image. Written for this tutorial: https://dev.to/jimutt/generate-merged-geotiff-imagery-from-web-maps-xyz-tile-servers-with-python-4d13

Extended with exception handling in case of requesting of missing tiles.

## Prerequisites:
- GDAL in Windows through OSGeo4W
- Empty "output" and "temp" folders in project directory. 

## Usage:
- Modify configuration in `tiles_to_tiff.py` according to personal preferences.
- On Windows use OSGeo4W Shell
- [Set environment for Python 3](https://gis.stackexchange.com/a/277842/12728) with `py3_env`
- Run script with `$ python3 tiles_to_tiff.py`

For more information see the accompanying dev.to post. 
