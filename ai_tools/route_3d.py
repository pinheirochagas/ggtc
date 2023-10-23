#%%

import gpxpy
import folium

# Parse the GPX file
def parse_gpx(gpx_file):
    with open(gpx_file, 'r') as file:
        gpx = gpxpy.parse(file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append(tuple([point.latitude, point.longitude]))
        return points

# Create the folium map
def create_map(gpx_points, map_center, zoom_start=12, tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"):
    m = folium.Map(location=map_center, zoom_start=zoom_start, tiles=tiles, attr='ESRI')
    folium.PolyLine(gpx_points, color="blue", weight=2.5, opacity=1).add_to(m)
    return m

# Provide the path to your GPX file
gpx_file = '/Users/pinheirochagas/Downloads/mt_tam.gpx'


# Parse the GPX data
gpx_points = parse_gpx(gpx_file)

# Define the center of the map
map_center = gpx_points[0]

# Create the map with the GPX route
m = create_map(gpx_points, map_center)

# Show the map
m.save('gpx_route_map.html')

# %%
