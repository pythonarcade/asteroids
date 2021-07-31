import arcade
from bullet import Bullet


class GlowBall(Bullet):
    def __init__(self, shadertoy, glowcolor, radius):
        super().__init__(shadertoy=shadertoy)
        self.type = None
        self.shadertoy = shadertoy
        self.glowcolor = glowcolor
        self.texture = arcade.make_circle_texture(radius * 2, glowcolor)
        self._points = self.texture.hit_box_points

    def draw(self):
        self.shadertoy.program['pos'] = self.position
        self.shadertoy.program['color'] = arcade.get_three_float_color(self.glowcolor)
        self.shadertoy.render()
