import os
from .window import Window
from .scene import Scene
from .shader import Shader


class Engine:
    def __init__(self, width=800, height=600, title="3D Game Render Engine"):
        self.window = Window(width, height, title)
        self.scene = Scene()
        self.running = False
        self.last_time = 0
        self.delta_time = 0

        self.default_shader = None
        self._init_default_shader()
    #get shaders from shader dir
    def _init_default_shader(self):
        shaders_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shaders")
        vert_shader = os.path.join(shaders_dir, "phong.vert")
        frag_shader = os.path.join(shaders_dir, "phong.frag")
        self.default_shader = Shader(vert_shader, frag_shader)

    def start(self):
        import glfw
        self.running = True
        self.last_time = glfw.get_time()

        while self.running and not self.window.should_close():
            current_time = glfw.get_time()
            self.delta_time = current_time - self.last_time
            self.last_time = current_time
            self.window.poll_events()
            self.update(self.delta_time)
            self.render()
            self.window.swap_buffers()

        self.shutdown()

    def stop(self):
        self.running = False

    #only gets used by application
    def update(self, delta_time):
        pass

    def render(self):
        self.window.clear(0.1, 0.1, 0.1, 1.0)
        camera = self.scene.camera
        if not camera:
            return

        aspect_ratio = self.window.get_aspect_ratio()
        view_matrix = camera.get_view_matrix()
        projection_matrix = camera.get_projection_matrix(aspect_ratio)

        self.default_shader.use()
        self.default_shader.set_mat4("view", view_matrix)
        self.default_shader.set_mat4("projection", projection_matrix)
        self.default_shader.set_vec3("viewPos", camera.position)
        self.scene.render(self.default_shader)

    def shutdown(self):
        self.window.terminate()

    def get_delta_time(self):
        return self.delta_time

    def get_window(self):
        """Get the window"""
        return self.window

    def get_scene(self):
        """Get the scene"""
        return self.scene