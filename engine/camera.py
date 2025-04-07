import numpy as np
import pyrr


class Camera:
    def __init__(self, position=np.array([0.0, 0.0, 3.0], dtype=np.float32),
                 target=np.array([0.0, 0.0, 0.0], dtype=np.float32),
                 up=np.array([0.0, 1.0, 0.0], dtype=np.float32),
                 yaw=-90.0, pitch=0.0):
        self.position = np.array(position, dtype=np.float32)
        self.world_up = np.array(up, dtype=np.float32)
        self.yaw = yaw
        self.pitch = pitch
        self.zoom = 45.0

        if target is not None:
            target = np.array(target, dtype=np.float32)
            direction = target - self.position
            direction = direction / np.linalg.norm(direction)
            self.yaw = np.degrees(np.arctan2(direction[2], direction[0]))
            self.pitch = np.degrees(np.arcsin(direction[1]))

        self._update_camera_vectors()

    def _update_camera_vectors(self):
        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ], dtype=np.float32)
        self.front = front / np.linalg.norm(front)

        self.right = np.cross(self.front, self.world_up)
        self.right = self.right / np.linalg.norm(self.right)

        self.up = np.cross(self.right, self.front)
        self.up = self.up / np.linalg.norm(self.up)

    def get_view_matrix(self):
        return pyrr.matrix44.create_look_at(self.position, self.position + self.front, self.up)

    def get_projection_matrix(self, aspect_ratio):
        return pyrr.matrix44.create_perspective_projection(
            self.zoom, aspect_ratio, 0.1, 100.0
        )

    def set_position(self, position):
        self.position = np.array(position, dtype=np.float32)
        self._update_camera_vectors()


    # moving camera, is extremely yanky but does the job
    def move(self, direction, amount):
        if direction == "forward":
            self.position += self.front * amount
        elif direction == "backward":
            self.position -= self.front * amount
        elif direction == "left":
            self.position -= self.right * amount
        elif direction == "right":
            self.position += self.right * amount
        elif direction == "up":
            self.position += self.up * amount
        elif direction == "down":
            self.position -= self.up * amount

    def rotate(self, yaw_offset, pitch_offset, constrain_pitch=True):
        self.yaw += yaw_offset
        self.pitch += pitch_offset

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self._update_camera_vectors()

    # basically the fov
    def set_zoom(self, zoom):
        self.zoom = zoom
        if self.zoom < 1.0:
            self.zoom = 1.0
        if self.zoom > 45.0:
            self.zoom = 45.0