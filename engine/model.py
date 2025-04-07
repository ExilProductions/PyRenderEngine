import numpy as np
import pyrr
import open3d as o3d
from .mesh import Mesh
import os
from .obj_loader import load_obj


class Model:
    def __init__(self, path=None, mesh=None):
        self.meshes = []
        self.textures_loaded = {}
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.scale = np.array([1.0, 1.0, 1.0])
        self.color = np.array([0.8, 0.8, 0.8])
        self.shininess = 32.0

        if path:
            self._load_model(path)
        elif mesh:
            self.meshes.append(mesh)
        else:
            self._create_cube()

    def _load_model(self, path):
        directory = os.path.dirname(path)
        if path.lower().endswith('.obj'):
            mesh = load_obj(path, directory)
            self.meshes.append(mesh)
        elif path.lower().endswith('.ply'):
            o3d_mesh = o3d.io.read_triangle_mesh(path)
            if not o3d_mesh.has_vertex_normals():
                o3d_mesh.compute_vertex_normals()
            mesh = Mesh(o3d_mesh=o3d_mesh)
            self.meshes.append(mesh)
        elif path.lower().endswith('.stl'):
            o3d_mesh = o3d.io.read_triangle_mesh(path)
            if not o3d_mesh.has_vertex_normals():
                o3d_mesh.compute_vertex_normals()
            mesh = Mesh(o3d_mesh=o3d_mesh)
            self.meshes.append(mesh)
        else:
            self._create_cube()

    def _create_cube(self):
        mesh = Mesh.create_box()
        self.meshes.append(mesh)

    @staticmethod
    def create_box(width=1.0, height=1.0, depth=1.0):
        mesh = Mesh.create_box(width, height, depth)
        return Model(mesh=mesh)

    @staticmethod
    def create_sphere(radius=1.0, resolution=20):
        mesh = Mesh.create_sphere(radius, resolution)
        return Model(mesh=mesh)

    @staticmethod
    def create_cylinder(radius=1.0, height=2.0, resolution=20, split=4):
        mesh = Mesh.create_cylinder(radius, height, resolution, split)
        return Model(mesh=mesh)

    @staticmethod
    def create_cone(radius=1.0, height=2.0, resolution=20, split=1):
        mesh = Mesh.create_cone(radius, height, resolution, split)
        return Model(mesh=mesh)

    @staticmethod
    def create_torus(torus_radius=1.0, tube_radius=0.2, radial_resolution=30, tubular_resolution=20):
        mesh = Mesh.create_torus(torus_radius, tube_radius, radial_resolution, tubular_resolution)
        return Model(mesh=mesh)

    def set_color(self, color):
        self.color = np.array(color, dtype=np.float32)

    def set_shininess(self, shininess):
        self.shininess = shininess

    def draw(self, shader):
        model_matrix = np.identity(4, dtype=np.float32)
        model_matrix = pyrr.matrix44.create_from_scale(self.scale, dtype=np.float32)
        rotation_x = pyrr.matrix44.create_from_x_rotation(np.radians(self.rotation[0]), dtype=np.float32)
        rotation_y = pyrr.matrix44.create_from_y_rotation(np.radians(self.rotation[1]), dtype=np.float32)
        rotation_z = pyrr.matrix44.create_from_z_rotation(np.radians(self.rotation[2]), dtype=np.float32)
        rotation_matrix = pyrr.matrix44.multiply(rotation_x, rotation_y)
        rotation_matrix = pyrr.matrix44.multiply(rotation_matrix, rotation_z)
        model_matrix = pyrr.matrix44.multiply(model_matrix, rotation_matrix)
        translation = pyrr.matrix44.create_from_translation(self.position, dtype=np.float32)
        model_matrix = pyrr.matrix44.multiply(model_matrix, translation)
        shader.set_mat4("model", model_matrix)
        shader.set_float("material.shininess", self.shininess)
        shader.set_vec3("objectColor", self.color)

        for mesh in self.meshes:
            has_textures = len(mesh.textures) > 0
            shader.set_bool("hasTexture", has_textures)

            mesh.draw(shader)

    def set_position(self, position):
        self.position = position

    def set_rotation(self, rotation):
        self.rotation = rotation

    def set_scale(self, scale):
        self.scale = scale

    def rotate(self, axis, angle):
        if axis[0] > 0:
            self.rotation[0] += np.degrees(angle)
        if axis[1] > 0:
            self.rotation[1] += np.degrees(angle)
        if axis[2] > 0:
            self.rotation[2] += np.degrees(angle)