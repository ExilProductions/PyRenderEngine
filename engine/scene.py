from engine.light import PointLight


class Scene:
    def __init__(self):
        self.models = []
        self.lights = []
        self.camera = None

    def add_model(self, model):
        self.models.append(model)

    def add_light(self, light):
        self.lights.append(light)

    def set_camera(self, camera):
        self.camera = camera

    def render(self, shader):
        if not self.camera:
            raise ValueError("Camera not set in scene")
        #TODO: Actually do something with this boolean
        dir_light_set = False
        point_light_count = 0

        for light in self.lights:
            if isinstance(light, PointLight):
                light.apply(shader, point_light_count)
                point_light_count += 1
            else:
                light.apply(shader, 0)
                dir_light_set = True

        shader.set_int("numPointLights", point_light_count)

        for model in self.models:
            model.draw(shader)