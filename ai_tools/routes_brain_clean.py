#%%
import numpy as np
import matplotlib.pyplot as plt
import gpxpy
from nilearn import plotting, datasets, image
from scipy.ndimage import gaussian_filter

def generate_spiral(num_points=100, a=0.1, b=0.2, num_turns=2):
    """
    Generate a spiral in 2D (x, y) coordinates.
    
    Parameters:
        num_points (int): Number of points to generate for the spiral.
        a (float): Parameter controlling the distance between the spiral arms.
        b (float): Parameter controlling the tightness of the spiral turns.
        num_turns (int): Number of turns in the spiral.
    
    Returns:
        np.ndarray: Array of shape (num_points, 2) containing the (x, y) coordinates of the spiral.
    """
    theta_max = num_turns * 2 * np.pi
    theta = np.linspace(0, theta_max, num_points)
    r = a + b * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.column_stack((x, y))

# Generate the spiral coordinates
spiral_coords = generate_spiral()

# Plot the spiral coordinates
plt.figure(figsize=(6, 6))
plt.plot(spiral_coords[:, 0], spiral_coords[:, 1])
plt.title("Example GPX Coordinates (Spiral)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.axis("equal")
plt.show()

#%%
import gpxpy


def read_gpx_file(file_path):
    """
    Read a GPX file and extract the latitude and longitude coordinates.

    Parameters:
        file_path (str): Path to the GPX file.

    Returns:
        list: List of (latitude, longitude) tuples.
    """
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    coordinates = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinates.append((point.latitude, point.longitude))
    
    return coordinates

#%%
def transform_gpx_to_brain_coords(gpx_coords, scale_factor=0.5, translation=(50, 50)):
    """
    Transform GPX coordinates into the brain's coordinate system.
    
    Parameters:
        gpx_coords (np.ndarray): Array of shape (num_points, 2) containing the (x, y) coordinates of the GPX route.
        scale_factor (float): Scaling factor to adjust the size of the GPX route.
        translation (tuple): Translation values (dx, dy) to shift the GPX route to the desired location in the brain.
    
    Returns:
        np.ndarray: Array of shape (num_points, 3) containing the transformed coordinates in the brain's space.
    """
    # Normalize coordinates
    normalized_coords = (gpx_coords - gpx_coords.min(axis=0)) / (gpx_coords.max(axis=0) - gpx_coords.min(axis=0))

    # Scale and translate
    brain_coords = normalized_coords * scale_factor * np.array(mni_template.shape[:2])
    brain_coords += np.array(translation)
    
    # Set the X coordinate to a constant value (e.g., 50) for all points
    x_coord = np.full((brain_coords.shape[0], 1), 50)
    brain_coords = np.hstack((x_coord, brain_coords))
    
    return brain_coords

# Apply the revised transformation




# Read GPX file and transform coordinates
gpx_path = '/Users/pinheirochagas/Downloads/GGTC_50mi.gpx'  # Update with your GPX file path
gpx_coords = read_gpx_file(gpx_path)
gpx_array = np.array(gpx_coords)
brain_coords = transform_gpx_to_brain_coords(gpx_array)

# Normalize and scale brain coordinates to fit within the MNI template dimensions
mni_template = datasets.load_mni152_template()
normalized_brain_coords = np.copy(brain_coords)
normalized_brain_coords[:, 1] = (normalized_brain_coords[:, 1] - normalized_brain_coords[:, 1].min()) / (normalized_brain_coords[:, 1].max() - normalized_brain_coords[:, 1].min()) * (mni_template.shape[0] - 1)
normalized_brain_coords[:, 2] = (normalized_brain_coords[:, 2] - normalized_brain_coords[:, 2].min()) / (normalized_brain_coords[:, 2].max() - normalized_brain_coords[:, 2].min()) * (mni_template.shape[1] - 1)

# Create and modify the 3D NIfTI image
stat_map = np.zeros(mni_template.shape)
intensity_value = 10000
thickness = 1
for coord in normalized_brain_coords:
    x, y, z = map(int, coord)
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            for dz in range(-thickness, thickness + 1):
                if 0 <= x + dx < stat_map.shape[0] and 0 <= y + dy < stat_map.shape[1] and 0 <= z + dz < stat_map.shape[2]:
                    stat_map[x + dx, y + dy, z + dz] = intensity_value

# Apply Gaussian smoothing
smoothed_stat_map = gaussian_filter(stat_map, sigma=1)  # Adjust sigma for more or less smoothing

# Convert the smoothed array to a Nifti1Image and visualize
smoothed_stat_map_img = image.new_img_like(mni_template, smoothed_stat_map)
view = plotting.view_img_on_surf(smoothed_stat_map_img, surf_mesh='fsaverage', cmap='hot', symmetric_cmap=False, vmax=intensity_value)
view
# %%


from scipy.ndimage import affine_transform

# Define an affine transformation matrix
# This example matrix includes scaling and translation components
# Adjust the values based on the specific requirements of your data
transformation_matrix = np.array([[0.9, 0, 0],  # Scale factor for X-axis
                                  [0, 0.9, 0],  # Scale factor for Y-axis
                                  [0, 0, 0.9]]) # Scale factor for Z-axis

# Apply the transformation
transformed_stat_map = affine_transform(stat_map, transformation_matrix)

# Proceed with creating the Nifti1Image and visualization as before
smoothed_stat_map_img = image.new_img_like(mni_template, transformed_stat_map)
glass_brain_view = plotting.plot_glass_brain(smoothed_stat_map_img, display_mode='lyrz', colorbar=True, threshold=0.1, cmap='hot')

# %%
view = plotting.view_img(smoothed_stat_map_img)
view.open_in_browser()
# %%

import numpy as np
import pyvista as pv
from nilearn import datasets, surface

# Load fsaverage5 surface data
fsaverage = datasets.fetch_surf_fsaverage()

# For both hemispheres (left and right)
for hemi in ['left', 'right']:
    # Get the pial surface mesh (you can also use 'white' for white matter surface)
    surf_mesh = fsaverage['pial_' + hemi]

    # Load the surface data (vertices and faces)
    vertices, faces = surface.load_surf_mesh(surf_mesh)

    # Convert faces to PyVista format
    faces_pv = np.hstack([np.full((len(faces), 1), 3), faces]).ravel()

    # Create a PyVista PolyData object from the vertices and faces
    mesh = pv.PolyData(vertices, faces_pv)

    # Save the mesh as an STL file
    mesh.save(f'output_{hemi}.stl')
# %%
import numpy as np
import nibabel as nib
import pyvista as pv
from nilearn import plotting, surface, datasets

# Assuming 'smoothed_stat_map_img' is your statistical map
# and 'intensity_value' is a predefined intensity threshold

# Load fsaverage surface data
fsaverage = datasets.fetch_surf_fsaverage()

# For both hemispheres (left and right)
for hemi in ['left', 'right']:
    # Load the surface data (vertices and faces)
    vertices, faces = surface.load_surf_mesh(fsaverage['pial_' + hemi])

    # Map the statistical data to the surface
    texture = surface.vol_to_surf(smoothed_stat_map_img, fsaverage['pial_' + hemi], interpolation='linear')

    # Convert faces to PyVista format
    faces_pv = np.hstack([np.full((len(faces), 1), 3), faces]).ravel()

    # Create a PyVista PolyData object from the vertices, faces, and the statistical map
    mesh = pv.PolyData(vertices, faces_pv)
    mesh.point_arrays['Intensity'] = texture

    # Save the mesh as an STL file
    mesh.save(f'output_{hemi}.stl')
# %%
import numpy as np
import nibabel as nib
import pyvista as pv
from nilearn import plotting, surface, datasets

# Load fsaverage surface data
fsaverage = datasets.fetch_surf_fsaverage()

# Define a scale factor for the deformation
scale_factor = -1  # Adjust this factor as needed

# For both hemispheres (left and right)
for hemi in ['left', 'right']:
    # Load the surface data (vertices and faces)
    vertices, faces = surface.load_surf_mesh(fsaverage['pial_' + hemi])

    # Map the statistical data to the surface
    texture = surface.vol_to_surf(smoothed_stat_map_img, fsaverage['pial_' + hemi], interpolation='linear')

    # Normalize the texture data for deformation
    normalized_texture = (texture - texture.min()) / (texture.max() - texture.min())

    # Deform the mesh based on the statistical data
    deformed_vertices = vertices + vertices * normalized_texture[:, np.newaxis] * scale_factor

    # Convert faces to PyVista format
    faces_pv = np.hstack([np.full((len(faces), 1), 3), faces]).ravel()

    # Create a PyVista PolyData object from the deformed vertices and faces
    mesh = pv.PolyData(deformed_vertices, faces_pv)

    # Save the mesh as an STL file
    mesh.save(f'output_deformed_{hemi}.stl')

# %%
import vtk
from nilearn import surface, datasets

# Load fsaverage data
fsaverage = datasets.fetch_surf_fsaverage()

# Use the left hemisphere pial surface as an example
pial_surf_left = fsaverage['pial_left']


# Map the statistical data to the surface
texture_data = surface.vol_to_surf(smoothed_stat_map_img, pial_surf_left)

# Read the surface data
reader = vtk.vtkPolyDataReader()
reader.SetFileName(pial_surf_left)
reader.Update()

# Map the texture data to the surface
mesh = reader.GetOutput()
point_data = mesh.GetPointData()
scalars = vtk.vtkFloatArray()
for i in range(len(texture_data)):
    scalars.InsertTuple1(i, texture_data[i])
point_data.SetScalars(scalars)

# Create a mapper and actor
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(mesh)
mapper.ScalarVisibilityOn()
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Add the actor to the scene
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)  # Background color white

# Render and interact
renderWindow.Render()
renderWindowInteractor.Start()
# %%
renderWindowInteractor.Start()


# %%
