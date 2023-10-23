
#%%
import gpxpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to parse GPX file and extract latitude, longitude, and elevation points
def parse_gpx(gpx_file_path):
    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        lat = []
        lon = []
        ele = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    ele.append(point.elevation)
        return lat, lon, ele

# Load GPX files
lat1, lon1, ele1 = parse_gpx('/Users/pinheirochagas/Downloads/mt_tam.gpx')
lat2, lon2, ele2 = parse_gpx('/Users/pinheirochagas/Downloads/lighthouse.gpx')

# Plot 3D routes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(lon1, lat1, ele1, label='Route 1', color='blue')
ax.plot(lon2, lat2, ele2, label='Route 2', color='green')

# Determine intersection points and plot them in red
intersection_indices = set(zip(lat1, lon1, ele1)) & set(zip(lat2, lon2, ele2))
for intersection_point in intersection_indices:
    ax.scatter(intersection_point[1], intersection_point[0], intersection_point[2], color='red')

# Customize plot
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation')
ax.legend()

# Show plot
plt.show()

# %%
