import numpy as np

class Light:
    def __init__(self, ambient, diffuse, specular):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def apply(self, shader, index):
        pass

#here comes the sun duh duh duh duh
class DirectionalLight(Light):
    def __init__(self, direction, ambient, diffuse, specular):
        super().__init__(ambient, diffuse, specular)
        self.direction = direction

    def apply(self, shader, index):
        shader.set_vec3(f"dirLight.direction", self.direction)
        shader.set_vec3(f"dirLight.ambient", self.ambient)
        shader.set_vec3(f"dirLight.diffuse", self.diffuse)
        shader.set_vec3(f"dirLight.specular", self.specular)

#point light implementation
class PointLight(Light):
    def __init__(self, position, ambient, diffuse, specular, constant, linear, quadratic):
        super().__init__(ambient, diffuse, specular)
        self.position = position
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic

    def apply(self, shader, index):
        shader.set_vec3(f"pointLights[{index}].position", self.position)
        shader.set_vec3(f"pointLights[{index}].ambient", self.ambient)
        shader.set_vec3(f"pointLights[{index}].diffuse", self.diffuse)
        shader.set_vec3(f"pointLights[{index}].specular", self.specular)
        shader.set_float(f"pointLights[{index}].constant", self.constant)
        shader.set_float(f"pointLights[{index}].linear", self.linear)
        shader.set_float(f"pointLights[{index}].quadratic", self.quadratic)


class SpotLight(Light):
    def __init__(self, position, direction, ambient, diffuse, specular,
                 constant, linear, quadratic, cut_off, outer_cut_off):
        super().__init__(ambient, diffuse, specular)
        self.position = position
        self.direction = direction
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
        self.cut_off = cut_off
        self.outer_cut_off = outer_cut_off

    def apply(self, shader, index):
        shader.set_vec3(f"spotLight.position", self.position)
        shader.set_vec3(f"spotLight.direction", self.direction)
        shader.set_vec3(f"spotLight.ambient", self.ambient)
        shader.set_vec3(f"spotLight.diffuse", self.diffuse)
        shader.set_vec3(f"spotLight.specular", self.specular)
        shader.set_float(f"spotLight.constant", self.constant)
        shader.set_float(f"spotLight.linear", self.linear)
        shader.set_float(f"spotLight.quadratic", self.quadratic)
        shader.set_float(f"spotLight.cutOff", self.cut_off)
        shader.set_float(f"spotLight.outerCutOff", self.outer_cut_off)