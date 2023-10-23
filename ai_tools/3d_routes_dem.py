#%%
import gpxpy
import geopandas as gpd
from shapely.geometry import LineString

# Load the GPX file
with open('/Users/pinheirochagas/Downloads/mt_tam.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extract the route coordinates
coordinates = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            coordinates.append((point.longitude, point.latitude))

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame({'geometry': [LineString(coordinates)]})

# Optionally, you can reproject the data to match the CRS of the DEM
# gdf = gdf.to_crs(dem_crs)
bounds = gpx.get_bounds()
api_url = 'https://portal.opentopography.org/API/globaldem'
params = {
    'dem_type': 'SRTMGL3',   # DEM type (e.g., SRTM Global 1 arc second)
    'south': bounds.min_latitude,  # Southern boundary (latitude)
    'north': bounds.max_latitude,  # Northern boundary (latitude)
    'west': bounds.min_longitude,  # Western boundary (longitude)
    'east': bounds.max_longitude,  # Eastern boundary (longitude)
    'outputFormat': 'GTiff' # Output format (e.g., GeoTIFF)
    }

# %%
import matplotlib.pyplot as plt

from bmi_topography import Topography

params = Topography.DEFAULT.copy()
params["cache_dir"] = "."
params["south"] = params['south']
params["north"] = params['north']
params["west"] = params['west']
params["east"] = params['east']

boulder = Topography(**params)

boulder.fetch()
boulder.load()

boulder.da.spatial_ref

boulder.da.plot()
plt.show()

# %%

import rasterio
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Replace this with the path to your DEM TIFF file
dem_tif_file_path = 'dem.tif'

# Read the DEM data from the TIFF file
with rasterio.open(dem_tif_file_path) as src:
    dem_data = src.read(1)
    transform = src.transform
    
# Calculate X and Y coordinates based on the transform
x = np.arange(0, dem_data.shape[1]) * transform[0] + transform[2]
y = np.arange(0, dem_data.shape[0]) * transform[4] + transform[5]
x, y = np.meshgrid(x, y)

# Create a 3D plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, dem_data, cmap='terrain')

# Set plot labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Elevation')
ax.set_title('3D Plot of DEM')

# Show the plot
plt.show()


# %%
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import gpxpy

# Replace these paths with the paths to your files
dem_tif_file_path = 'dem.tif'
gpx_file_path = '/Users/pinheirochagas/Downloads/mt_tam.gpx'

# Read the DEM data from the TIFF file
with rasterio.open(dem_tif_file_path) as src:
    dem_data = src.read(1)
    transform = src.transform
    
# Calculate X and Y coordinates based on the transform
x = np.arange(0, dem_data.shape[1]) * transform[0] + transform[2]
y = np.arange(0, dem_data.shape[0]) * transform[4] + transform[5]
x, y = np.meshgrid(x, y)

# Create a 3D plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, dem_data, cmap='terrain')

# Read and parse the GPX file
with open(gpx_file_path, 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point_idx, point in enumerate(segment.points):
                # Convert lat/lon to raster coordinates
                row, col = src.index(point.longitude, point.latitude)
                # Get elevation from DEM data
                elev = dem_data[row, col]
                # Plot the point on the 3D plot
                ax.scatter(point.longitude, point.latitude, elev, c='red', marker='o')

# Set plot labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Elevation')
ax.set_title('3D Plot of DEM with GPX Route')

# Show the plot
plt.show()

# %%
