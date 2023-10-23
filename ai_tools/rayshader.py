#%%
import tempfile
import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
import rpy2.robjects as ro
import rpy2.robjects.numpy2ri
import rpy2.robjects.packages as rpackages

rpy2.robjects.numpy2ri.activate()
# %%
zip_url = '/vsizip//vsicurl/https://tylermw.com/data/dem_01.tif.zip/dem_01.tif'
with rio.open(zip_url) as f:
    z = f.read(1)
    
plt.imshow(z)
# %%
def rayshade(z, img_path=None, zscale=10, fov=0, theta=135, zoom=0.75, phi=45, windowsize=(1000, 1000)):
    
    # Output path.
    if not img_path:
        img_path = tempfile.NamedTemporaryFile(suffix='.png').name
    
    # Import needed packages.
    rayshader = rpackages.importr('rayshader')
    
    # Convert array to matrix.
    z = np.asarray(z)
    rows, cols = z.shape
    z_mat = ro.r.matrix(z, nrow=rows, ncol=cols)
    ro.globalenv['elmat'] = z_mat
    
    # Save python state to r.
    ro.globalenv['img_path'] = img_path
    ro.globalenv['zscale'] = zscale
    ro.globalenv['fov'] = fov
    ro.globalenv['theta'] = theta
    ro.globalenv['zoom'] = zoom
    ro.globalenv['phi'] = phi
    ro.globalenv['windowsize'] = ro.IntVector(windowsize)
    
    # Do the render.
    ro.r('''
        elmat %>%
          sphere_shade(texture = "desert") %>%
          add_water(detect_water(elmat), color = "desert") %>%
          add_shadow(ray_shade(elmat, zscale = 3), 0.5) %>%
          add_shadow(ambient_shade(elmat), 0) %>%
          plot_3d(elmat, zscale = zscale, fov = fov, theta = theta, zoom = zoom, phi = phi, windowsize = windowsize)
        Sys.sleep(0.2)
        render_snapshot(img_path)
    ''')
    
    # Return path.
    return img_path
# %%
img_path = rayshade(z)

from IPython.display import Image
Image(filename=img_path) 
# %%
