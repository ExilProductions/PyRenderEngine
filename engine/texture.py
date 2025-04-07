from OpenGL.GL import *
from PIL import Image
import numpy as np


class Texture:
    def __init__(self, path, type_name="texture_diffuse"):
        self.id = glGenTextures(1)
        self.type = type_name
        self.path = path
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(image.getdata()), np.uint8)
        if image.mode == "RGB":
            img_format = GL_RGB
        elif image.mode == "RGBA":
            img_format = GL_RGBA
        else:
            raise ValueError(f"Unsupported image format: {image.mode}")
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D, 0, img_format, image.width, image.height, 0,
            img_format, GL_UNSIGNED_BYTE, img_data
        )
        glGenerateMipmap(GL_TEXTURE_2D)
        image.close()