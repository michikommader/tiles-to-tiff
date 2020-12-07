import math
import urllib.request
import os
import glob
import subprocess
import shutil
from tile_convert import bbox_to_xyz, tile_edges
from osgeo import gdal

#---------- CONFIGURATION -----------#
tile_server = "file:///D:/path_to/local_tiles/{z}/{x}/{y}.png"
temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
output_dir = os.path.join(os.path.dirname(__file__), 'output')
zoom = 20
lon_min = 10.230949974
lon_max = 11.085477802
lat_min = 52.183009959
lat_max = 52.483249467
#-----------------------------------#

def download_tile(x, y, z, tile_server):
    url = tile_server.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    path = f'{temp_dir}/{x}_{y}_{z}.png'
    urllib.request.urlretrieve(url, path)
    return(path)


def merge_tiles(input_pattern, output_path):
    merge_command = ['gdal_merge.py', '-o', output_path]
	
    for name in glob.glob(input_pattern):
        merge_command.append(name)

    subprocess.call(merge_command)


def georeference_raster_tile(x, y, z, path):
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)


x_min, x_max, y_min, y_max = bbox_to_xyz(
    lon_min, lon_max, lat_min, lat_max, zoom)

print(f"Fetching {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")

for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
        try:
            png_path = download_tile(x, y, zoom, tile_server)
            #print(f"{x},{y} fetched")
            georeference_raster_tile(x, y, zoom, png_path)
        except OSError:
            #print(f"{x},{y} missing")
            pass


print("Download complete")

print("Merging tiles")
merge_tiles(temp_dir + '/*.tif', output_dir + '/merged.tif')
print("Merge complete")

shutil.rmtree(temp_dir)
os.makedirs(temp_dir)
