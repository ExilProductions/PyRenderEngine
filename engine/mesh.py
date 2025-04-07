from OpenGL.GL import *
import numpy as np
import open3d as o3d
import ctypes


class Mesh:
    def __init__(self, o3d_mesh=None, vertices=None, indices=None, textures=None):
        self.textures = textures if textures else []
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        #if we use a mesh from open3d we should use vertices and indices

        if o3d_mesh is not None:
            self._init_from_open3d(o3d_mesh)
        #if not just use the vertices and indices
        elif vertices is not None and indices is not None:
            self._init_from_arrays(vertices, indices)
        else:
            raise ValueError("Either an Open3D mesh or vertices and indices must be provided")

    def _init_from_open3d(self, o3d_mesh):
        if not o3d_mesh.has_vertex_normals():
            o3d_mesh.compute_vertex_normals()
        vertices = np.asarray(o3d_mesh.vertices)
        normals = np.asarray(o3d_mesh.vertex_normals)

        if o3d_mesh.has_triangle_uvs():
            uvs = np.asarray(o3d_mesh.triangle_uvs)
            #this is only some workaround though, still need to implement this right
            if len(uvs) > 0:
                tex_coords = np.zeros((len(vertices), 2), dtype=np.float32)
                for i, triangle in enumerate(o3d_mesh.triangles):
                    for j in range(3):
                        tex_coords[triangle[j]] = uvs[i * 3 + j]
            else:
                tex_coords = np.zeros((len(vertices), 2), dtype=np.float32)
        else:
            tex_coords = np.zeros((len(vertices), 2), dtype=np.float32)
        vertex_data = np.zeros((len(vertices), 8), dtype=np.float32)
        vertex_data[:, 0:3] = vertices
        vertex_data[:, 3:6] = normals
        vertex_data[:, 6:8] = tex_coords

        indices = np.asarray(o3d_mesh.triangles).flatten()

        self._init_from_arrays(vertex_data, indices)

        self.o3d_mesh = o3d_mesh

    def _init_from_arrays(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)

    @staticmethod
    def create_box(width=1.0, height=1.0, depth=1.0):
        box = o3d.geometry.TriangleMesh.create_box(width=width, height=height, depth=depth)
        box.compute_vertex_normals()
        return Mesh(o3d_mesh=box)

    @staticmethod
    def create_sphere(radius=1.0, resolution=20):
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=radius, resolution=resolution)
        sphere.compute_vertex_normals()
        return Mesh(o3d_mesh=sphere)

    @staticmethod
    def create_cylinder(radius=1.0, height=2.0, resolution=20, split=4):
        cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=height, resolution=resolution,
                                                             split=split)
        cylinder.compute_vertex_normals()
        return Mesh(o3d_mesh=cylinder)

    @staticmethod
    def create_cone(radius=1.0, height=2.0, resolution=20, split=1):
        cone = o3d.geometry.TriangleMesh.create_cone(radius=radius, height=height, resolution=resolution, split=split)
        cone.compute_vertex_normals()
        return Mesh(o3d_mesh=cone)

    @staticmethod
    def create_torus(torus_radius=1.0, tube_radius=0.2, radial_resolution=30, tubular_resolution=20):
        torus = o3d.geometry.TriangleMesh.create_torus(torus_radius=torus_radius, tube_radius=tube_radius,
                                                       radial_resolution=radial_resolution,
                                                       tubular_resolution=tubular_resolution)
        torus.compute_vertex_normals()
        return Mesh(o3d_mesh=torus)

    def draw(self, shader):
        diffuse_nr = 1
        specular_nr = 1

        for i, texture in enumerate(self.textures):
            glActiveTexture(GL_TEXTURE0 + i)
            number = ""
            name = texture.type
            if name == "texture_diffuse":
                number = str(diffuse_nr)
                diffuse_nr += 1
            elif name == "texture_specular":
                number = str(specular_nr)
                specular_nr += 1

            shader.set_int(f"material.{name}{number}", i)

            glBindTexture(GL_TEXTURE_2D, texture.id)

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glActiveTexture(GL_TEXTURE0)