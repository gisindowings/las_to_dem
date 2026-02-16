import laspy
import numpy as np
import rasterio
from rasterio.transform import from_origin
from scipy.interpolate import griddata

# 1. Read LAS
las = laspy.read("point_cloud.las")

x = las.x
y = las.y
z = las.z

# 2. Define raster resolution (meters / units)
res = 1.0  # change to 0.5 or 2.0 if needed

# 3. Define raster extent
xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

# 4. Create grid
grid_x, grid_y = np.meshgrid(
    np.arange(xmin, xmax, res),
    np.arange(ymin, ymax, res)
)

# 5. Interpolate Z values (DSM)
grid_z = griddata(
    (x, y),
    z,
    (grid_x, grid_y),
    method="nearest"   # fastest & safest for DSM
)

# 6. Define transform
transform = from_origin(xmin, ymax, res, res)

# 7. Write GeoTIFF
with rasterio.open(
    "dsm.tif",
    "w",
    driver="GTiff",
    height=grid_z.shape[0],
    width=grid_z.shape[1],
    count=1,
    dtype=grid_z.dtype,
    crs=None,          # local coordinates (important!)
    transform=transform,
) as dst:
    dst.write(grid_z, 1)

print(".las is written to dsm.tif")

