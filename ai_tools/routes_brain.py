#%%
import numpy as np
import matplotlib.pyplot as plt

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
def transform_gpx_to_brain_coords(gpx_coords, scale_factor=10, translation=(50, 50)):
    """
    Transform GPX coordinates into the brain's coordinate system.
    
    Parameters:
        gpx_coords (np.ndarray): Array of shape (num_points, 2) containing the (x, y) coordinates of the GPX route.
        scale_factor (float): Scaling factor to adjust the size of the GPX route.
        translation (tuple): Translation values (dx, dy) to shift the GPX route to the desired location in the brain.
    
    Returns:
        np.ndarray: Array of shape (num_points, 3) containing the transformed coordinates in the brain's space.
    """
    brain_coords = scale_factor * gpx_coords
    brain_coords += np.array(translation)
    
    # Project the transformed 2D coordinates onto a coronal slice (Y-Z plane) of the brain
    # Set the X coordinate to a constant value (e.g., 50) for all points
    x_coord = np.full((brain_coords.shape[0], 1), 50)
    brain_coords = np.hstack((x_coord, brain_coords))
    
    return brain_coords

# Transform the spiral GPX coordinates into brain coordinates
brain_coords = transform_gpx_to_brain_coords(spiral_coords)

# Plot the transformed coordinates in the brain's space
plt.figure(figsize=(6, 6))
plt.plot(brain_coords[:, 1], brain_coords[:, 2])
plt.title("Transformed GPX Coordinates in Brain's Space")
plt.xlabel("Y Coordinate (MNI)")
plt.ylabel("Z Coordinate (MNI)")
plt.axis("equal")
plt.show()


# %%
from nilearn import plotting, datasets, image
import numpy as np

# Load the MNI152 template
mni_template = datasets.load_mni152_template()

# Create a 3D NIfTI image with zeros (background)
stat_map = np.zeros(mni_template.shape)

# Set the voxels corresponding to the transformed GPX route to a high value (e.g., 1000)
for coord in brain_coords:
    x, y, z = coord.astype(int)
    stat_map[x, y, z] = 1000

# Convert the numpy array to a Nifti1Image
stat_map_img = image.new_img_like(mni_template, stat_map)

# Use view_img_on_surf to project the NIfTI image onto the brain surface
view = plotting.view_img_on_surf(stat_map_img, threshold='80%', surf_mesh='fsaverage', cmap='jet', symmetric_cmap=False)

# Display the interactive plot
view








# %%
