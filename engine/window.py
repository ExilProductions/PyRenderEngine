import glfw
from OpenGL.GL import *


class Window:
    def __init__(self, width, height, title):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")
        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, self._framebuffer_size_callback)
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        self.width = width
        self.height = height

        self.last_x = width / 2
        self.last_y = height / 2
        self.first_mouse = True
        self.keys = {}

        self.x_offset = 0
        self.y_offset = 0

        glfw.set_cursor_pos_callback(self.window, self._mouse_callback)
        glfw.set_key_callback(self.window, self._key_callback)
        glfw.set_scroll_callback(self.window, self._scroll_callback)

        self.mouse_buttons = {}
        glfw.set_mouse_button_callback(self.window, self._mouse_button_callback)

        self.scroll_offset = 0

    def _framebuffer_size_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        self.width = width
        self.height = height

    def _mouse_callback(self, window, xpos, ypos):
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        self.x_offset = xpos - self.last_x
        self.y_offset = self.last_y - ypos

        self.last_x = xpos
        self.last_y = ypos

    def _key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def _mouse_button_callback(self, window, button, action, mods):
        if action == glfw.PRESS:
            self.mouse_buttons[button] = True
        elif action == glfw.RELEASE:
            self.mouse_buttons[button] = False

    def _scroll_callback(self, window, xoffset, yoffset):
        self.scroll_offset = yoffset

    def is_key_pressed(self, key):
        return key in self.keys and self.keys[key]

    def is_mouse_button_pressed(self, button):
        return button in self.mouse_buttons and self.mouse_buttons[button]

    def get_mouse_position(self):
        return glfw.get_cursor_pos(self.window)

    def get_mouse_offset(self):
        offset = (self.x_offset, self.y_offset)
        self.x_offset = 0
        self.y_offset = 0
        return offset

    def get_scroll_offset(self):
        offset = self.scroll_offset
        self.scroll_offset = 0
        return offset

    def poll_events(self):
        glfw.poll_events()

    def should_close(self):
        return glfw.window_should_close(self.window)

    def set_should_close(self, value):
        glfw.set_window_should_close(self.window, value)

    def clear(self, r, g, b, a):
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def terminate(self):
        glfw.terminate()

    def get_aspect_ratio(self):
        return self.width / self.height

    def set_cursor_mode(self, mode):
        glfw.set_input_mode(self.window, glfw.CURSOR, mode)