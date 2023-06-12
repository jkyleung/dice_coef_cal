import numpy as np
import open3d as o3d

# const.
PCD_METHOD = 0
VECTICES_METHOD = 1
MAX_BOUND = [300]*3
MIN_BOUND = [-300]*3

# global var.
VOXEL_SIZE = 0.05
NUM_SAMPLE_PT = 100000

def mesh_to_voxel_grid(mesh, num_sample_pt=NUM_SAMPLE_PT, v_size=VOXEL_SIZE, method=PCD_METHOD):
    # input: stf file path, sampling points for point-cloud convertion, voxel size
    # output: voxel_grid object

    # PCD_METHOD
    # trun method, but running time is slow
    if method==PCD_METHOD:
        pcd = mesh.sample_points_poisson_disk(num_sample_pt)
        bound_box = o3d.geometry.AxisAlignedBoundingBox()
        bound_box.max_bound = MAX_BOUND
        bound_box.min_bound = MIN_BOUND
        pcd = pcd.crop(bound_box)
        voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=v_size)
        
    # VECTICES_METHOD
    # using vertices of mesh as the points of pcd
    elif method==VECTICES_METHOD:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(mesh.vertices)
        bound_box = o3d.geometry.AxisAlignedBoundingBox()
        bound_box.max_bound = MAX_BOUND
        bound_box.min_bound = MIN_BOUND + 1
        pcd = pcd.crop(bound_box)
        voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud_within_bounds(pcd, v_size, bound_box.min_bound, bound_box.max_bound)
    
    else:
        raise("ERROR: unknown method type")
    
    return voxel_grid

def dice_coef_calculation(model1, model2):
    # only 0 or 1 value for each voxel
    TP = np.where(model1==1 and model2==1, 1, 0)
    FP = np.where(model1==1 and model2==0, 1, 0)
    FN = np.where(model1==0 and model2==1, 1, 0)

    dice_coef = (2 * TP) / (2 * TP + FP + FN)

    return dice_coef

if __name__ == "__main__":
    
    ### Debug

    # load model 
    mesh = o3d.geometry.TriangleMesh.create_sphere(radius=5, resolution=100)
    # mesh = o3d.io.read_triangle_mesh(stl_path)
    
    # change mesh to np.array
    # 1> 3d slicer, mech to labelmap
    # 2> 3-matic
    # 3> stl-to-voxel library
    
    # voxelization
    print('voxelization')
    # voxel_grid = mesh_to_voxel_grid(mesh)
    voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh, voxel_size=0.05)
    o3d.visualization.draw_geometries([voxel_grid])
    
    # calculate DICE and print
    dice_coef = dice_coef_calculation(model1, model2)
    print(dice_coef)
