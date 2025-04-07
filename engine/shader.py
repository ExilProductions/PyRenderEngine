from OpenGL.GL import *

class Shader:
    def __init__(self, vertex_path, fragment_path):
        with open(vertex_path, 'r') as file:
            vertex_source = file.read()

        with open(fragment_path, 'r') as file:
            fragment_source = file.read()

        vertex_shader = self._compile_shader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = self._compile_shader(fragment_source, GL_FRAGMENT_SHADER)

        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            info_log = glGetProgramInfoLog(self.program)
            glDeleteProgram(self.program)
            glDeleteShader(vertex_shader)
            glDeleteShader(fragment_shader)
            raise RuntimeError(f"Shader program linking failed: {info_log}")
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def _compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            info_log = glGetShaderInfoLog(shader)
            glDeleteShader(shader)
            shader_type_name = "vertex" if shader_type == GL_VERTEX_SHADER else "fragment"
            raise RuntimeError(f"{shader_type_name} shader compilation failed: {info_log}")

        return shader

    def use(self):
        glUseProgram(self.program)

    def set_bool(self, name, value):
        glUniform1i(glGetUniformLocation(self.program, name), int(value))

    def set_int(self, name, value):
        glUniform1i(glGetUniformLocation(self.program, name), value)

    def set_float(self, name, value):
        glUniform1f(glGetUniformLocation(self.program, name), value)

    def set_vec2(self, name, value):
        glUniform2fv(glGetUniformLocation(self.program, name), 1, value)

    def set_vec3(self, name, value):
        glUniform3fv(glGetUniformLocation(self.program, name), 1, value)

    def set_vec4(self, name, value):
        glUniform4fv(glGetUniformLocation(self.program, name), 1, value)

    def set_mat2(self, name, value):
        glUniformMatrix2fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, value)

    def set_mat3(self, name, value):
        glUniformMatrix3fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, value)

    def set_mat4(self, name, value):
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, value)