import arcade


class Bullet(arcade.Sprite):
    def __init__(self, image_file=None, scale=1.0, shadertoy=None):
        super().__init__(image_file, scale)
        self.type = None
        self.shadertoy = shadertoy

    def draw(self):
        pass
