import numpy as np
import os
import glfw
from engine.engine import Engine
from engine.camera import Camera
from engine.model import Model
from engine.light import DirectionalLight, PointLight


class GameApp(Engine):
    def __init__(self, width=800, height=600, title="3D Game Demo"):
        super().__init__(width, height, title)

        self.camera = Camera(position=np.array([0, 2, 5]), target=np.array([0, 0, 0]))
        self.scene.set_camera(self.camera)

        self.camera_speed = 6
        self.mouse_sensitivity = 0.2

        self.window.set_cursor_mode(glfw.CURSOR_DISABLED)
        dir_light = DirectionalLight(
            direction=np.array([-0.2, -1.0, -0.3]),
            ambient=np.array([0.2, 0.2, 0.2]),
            diffuse=np.array([0.5, 0.5, 0.5]),
            specular=np.array([1.0, 1.0, 1.0])
        )
        self.scene.add_light(dir_light)

        point_light = PointLight(
            position=np.array([1.0, 1.0, 1.0]),
            ambient=np.array([0.1, 0.1, 0.1]),
            diffuse=np.array([0.8, 0.8, 0.8]),
            specular=np.array([1.0, 1.0, 1.0]),
            constant=1.0,
            linear=0.09,
            quadratic=0.032
        )
        self.scene.add_light(point_light)

        self.create_models()

    def create_models(self):
        cube_model = Model.create_box(1.0, 1.0, 1.0)
        cube_model.set_position(np.array([-1.5, 0, 0]))
        cube_model.set_color([0.8, 0.2, 0.2])  # Red
        cube_model.set_shininess(64.0)
        self.scene.add_model(cube_model)
        self.cube_model = cube_model

        sphere_model = Model.create_sphere(0.5, 32)
        sphere_model.set_position(np.array([0, 0, 0]))
        sphere_model.set_color([0.2, 0.8, 0.2])  # Green
        sphere_model.set_shininess(128.0)
        self.scene.add_model(sphere_model)
        self.sphere_model = sphere_model

        cylinder_model = Model.create_cylinder(0.5, 1.0, 32)
        cylinder_model.set_position(np.array([1.5, 0, 0]))
        cylinder_model.set_color([0.2, 0.2, 0.8])  # Blue
        cylinder_model.set_shininess(32.0)
        self.scene.add_model(cylinder_model)
        self.cylinder_model = cylinder_model

        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        obj_path = os.path.join(assets_dir, "cube.obj")

        if os.path.exists(obj_path):
            try:
                obj_model = Model(obj_path)
                obj_model.set_position(np.array([0, 1.5, 0]))
                obj_model.set_scale(np.array([0.5, 0.5, 0.5]))
                self.scene.add_model(obj_model)
                self.obj_model = obj_model
            except Exception as e:
                print(f"Could not load model: {e}")
        else:
            print(f"Model file not found: {obj_path}")
            torus_model = Model.create_torus(0.5, 0.2, 30, 20)
            torus_model.set_position(np.array([0, 1.5, 0]))
            self.scene.add_model(torus_model)
            self.torus_model = torus_model
            torus_model.set_color([0.8, 0.8, 0.2])
            torus_model.set_shininess(16.0)

    def update(self, delta_time):
        self.process_keyboard(delta_time)
        self.process_mouse()
        self.process_scroll()
        self.cube_model.rotate(np.array([0, 1, 0]), 0.5 * delta_time)
        self.sphere_model.rotate(np.array([1, 1, 0]), 0.3 * delta_time)
        self.cylinder_model.rotate(np.array([0, 0, 1]), 0.7 * delta_time)

        if self.window.is_key_pressed(glfw.KEY_ESCAPE):
            self.window.set_should_close(True)
    def process_keyboard(self, delta_time):
        velocity = self.camera_speed * delta_time

        if self.window.is_key_pressed(glfw.KEY_W):
            self.camera.move("forward", velocity)
        if self.window.is_key_pressed(glfw.KEY_S):
            self.camera.move("backward", velocity)
        if self.window.is_key_pressed(glfw.KEY_A):
            self.camera.move("left", velocity)
        if self.window.is_key_pressed(glfw.KEY_D):
            self.camera.move("right", velocity)
        if self.window.is_key_pressed(glfw.KEY_SPACE):
            self.camera.move("up", velocity)
        if self.window.is_key_pressed(glfw.KEY_LEFT_SHIFT):
            self.camera.move("down", velocity)

    def process_mouse(self):
        x_offset, y_offset = self.window.get_mouse_offset()
        if x_offset != 0 or y_offset != 0:
            x_offset *= self.mouse_sensitivity
            y_offset *= self.mouse_sensitivity
            self.camera.rotate(x_offset, y_offset)

    def process_scroll(self):
        y_offset = self.window.get_scroll_offset()
        if y_offset != 0:
            current_zoom = self.camera.zoom
            self.camera.set_zoom(current_zoom - y_offset)

def main():
    game = GameApp(800, 600, "3D Game Engine Demo")
    game.start()

if __name__ == "__main__":
    main()
