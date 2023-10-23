import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import folium

def load_gpx_file(file_path):
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
    return points

def find_intersections(points1, points2):
    return list(set(points1) & set(points2))

def plot_gpx_files(gpx_file1, gpx_file2):
    points1 = load_gpx_file(gpx_file1)
    points2 = load_gpx_file(gpx_file2)
    intersections = find_intersections(points1, points2)

    # Plotting the points and intersections using matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot([p[1] for p in points1], [p[0] for p in points1], 'b-', label='GPX1')
    plt.plot([p[1] for p in points2], [p[0] for p in points2], 'g-', label='GPX2')
    plt.plot([p[1] for p in intersections], [p[0] for p in intersections], 'ro', label='Intersections')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()

    # Plotting the points and intersections on the geographic map using folium
    map_center = intersections[0] if intersections else points1[0]
    gpx_map = folium.Map(location=map_center, zoom_start=14)
    folium.PolyLine(points1, color='blue', weight=2.5, opacity=1).add_to(gpx_map)
    folium.PolyLine(points2, color='green', weight=2.5, opacity=1).add_to(gpx_map)
    for point in intersections:
        folium.CircleMarker(location=point, radius=5, color='red', fill=True, fill_color='red').add_to(gpx_map)
    return gpx_map

# Provide the paths to your GPX files
gpx_file1 = '/Users/pinheirochagas/Downloads/mt_tam.gpx'
gpx_file2 = '/Users/pinheirochagas/Downloads/lighthouse.gpx'

# Plot the GPX files and intersections
gpx_map = plot_gpx_files(gpx_file1, gpx_file2)
gpx_map.save('gpx_map.html')  # Save the map to an HTML file
