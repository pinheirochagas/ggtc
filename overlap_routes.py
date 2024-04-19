#%%
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
import folium

#%%

def load_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        return points

def is_overlapping(point, route, threshold=0.0001):
    for route_point in route:
        if abs(point[0] - route_point[0]) < threshold and abs(point[1] - route_point[1]) < threshold:
            return True
    return False

def find_overlaps(route1, route2):
    overlaps = []
    for point in route1:
        if is_overlapping(point, route2):
            overlaps.append(point)
    return overlaps

#%%


# Load the GPX files
route1 = load_gpx('/Users/pinheirochagas/Downloads/cof.gpx')
route2 = load_gpx('/Users/pinheirochagas/Downloads/noe.gpx')


def load_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        return points


# Initialize the map to the first point of the first route
m = folium.Map(location=route1[0], zoom_start=13)

# Add routes to the map
folium.PolyLine(route1, color="blue", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(route2, color="green", weight=2.5, opacity=1).add_to(m)

# Save map to an HTML file
m.save("map.html")

# %%
import gpxpy
import folium
from geopy.distance import great_circle

def load_gpx(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        return points

def find_overlaps(route1, route2, max_distance=10):
    overlaps = []
    for point1 in route1:
        for point2 in route2:
            if great_circle(point1, point2).meters <= max_distance:
                overlaps.append(point1)
                break
    return overlaps


# Find overlapping points (within 10 meters)
overlaps = find_overlaps(route1, route2)

# Initialize the map at the first point of the first route
m = folium.Map(location=route1[0], zoom_start=14)

# Add routes to the map
folium.PolyLine(route1, color="blue", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(route2, color="green", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(overlaps, color="red", weight=2.5, opacity=1).add_to(m)

# Save map to an HTML file
m.save("map.html")

# %%
