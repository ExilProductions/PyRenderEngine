import open3d as o3d
import numpy as np
from .mesh import Mesh


def mesh_from_point(points, normals=None, colors=None):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    if normals is not None:
        pcd.normals = o3d.utility.Vector3dVector(normals)
    else:
        pcd.estimate_normals()
    if colors is not None:
        pcd.colors = o3d.utility.Vector3dVector(colors)
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8)
    return Mesh(o3d_mesh=mesh)


def merge_meshes(meshes):
    if not meshes:
        return None

    o3d_meshes = []
    for mesh in meshes:
        if hasattr(mesh, 'o3d_mesh'):
            o3d_meshes.append(mesh.o3d_mesh)
        else:
            o3d_meshes.append(mesh)

    merged_mesh = o3d_meshes[0]
    for mesh in o3d_meshes[1:]:
        merged_mesh += mesh
    if not merged_mesh.has_vertex_normals():
        merged_mesh.compute_vertex_normals()

    return Mesh(o3d_mesh=merged_mesh)

def subdivide_mesh(mesh, iterations=1):
    if hasattr(mesh, 'o3d_mesh'):
        o3d_mesh = mesh.o3d_mesh
    else:
        o3d_mesh = mesh
    subdivided_mesh = o3d_mesh.subdivide_midpoint(number_of_iterations=iterations)

    if not subdivided_mesh.has_vertex_normals():
        subdivided_mesh.compute_vertex_normals()
    return Mesh(o3d_mesh=subdivided_mesh)

#basically decimate
def simplify_mesh(mesh, target_triangles):
    if hasattr(mesh, 'o3d_mesh'):
        o3d_mesh = mesh.o3d_mesh
    else:
        o3d_mesh = mesh

    simplified_mesh = o3d_mesh.simplify_quadric_decimation(target_number_of_triangles=target_triangles)

    if not simplified_mesh.has_vertex_normals():
        simplified_mesh.compute_vertex_normals()

    return Mesh(o3d_mesh=simplified_mesh)

def create_terrain(width, length, height_function, resolution=100):
    x = np.linspace(-width / 2, width / 2, resolution)
    z = np.linspace(-length / 2, length / 2, resolution)
    X, Z = np.meshgrid(x, z)
    Y = np.zeros_like(X)
    for i in range(resolution):
        for j in range(resolution):
            Y[i, j] = height_function(X[i, j], Z[i, j])
    vertices = []
    for i in range(resolution):
        for j in range(resolution):
            vertices.append([X[i, j], Y[i, j], Z[i, j]])
    triangles = []
    for i in range(resolution - 1):
        for j in range(resolution - 1):
            idx1 = i * resolution + j
            idx2 = i * resolution + (j + 1)
            idx3 = (i + 1) * resolution + j
            idx4 = (i + 1) * resolution + (j + 1)

            triangles.append([idx1, idx2, idx3])
            triangles.append([idx2, idx4, idx3])

    o3d_mesh = o3d.geometry.TriangleMesh()
    o3d_mesh.vertices = o3d.utility.Vector3dVector(vertices)
    o3d_mesh.triangles = o3d.utility.Vector3iVector(triangles)
    o3d_mesh.compute_vertex_normals()

    return Mesh(o3d_mesh=o3d_mesh)