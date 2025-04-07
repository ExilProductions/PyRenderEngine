import numpy as np
import open3d as o3d
from .mesh import Mesh
from .texture import Texture
import os


def load_obj(file_path, directory=""):
    mesh = o3d.io.read_triangle_mesh(file_path)
    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()
    textures = []
    mtl_path = file_path.replace('.obj', '.mtl')
    if os.path.exists(mtl_path):
        with open(mtl_path, 'r') as f:
            current_material = None
            for line in f:
                if line.startswith('newmtl'):
                    current_material = line.split()[1]
                elif line.startswith('map_Kd') and current_material:
                    tex_path = os.path.join(directory, line.split()[1])
                    if os.path.exists(tex_path):
                        diffuse_texture = Texture(tex_path, "texture_diffuse")
                        textures.append(diffuse_texture)
                elif line.startswith('map_Ks') and current_material:
                    tex_path = os.path.join(directory, line.split()[1])
                    if os.path.exists(tex_path):
                        specular_texture = Texture(tex_path, "texture_specular")
                        textures.append(specular_texture)

    # Create and return the mesh with textures
    return Mesh(o3d_mesh=mesh, textures=textures)