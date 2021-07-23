import arcade
from arcade.experimental.shadertoy import Shadertoy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template Simple"


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)
        self.bullet_list: arcade.SpriteList = arcade.SpriteList()

        file_name = "glow.glsl"
        file = open(file_name)
        shader_sourcecode = file.read()
        size = width, height
        self.shadertoy = Shadertoy(size, shader_sourcecode)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        for bullet in self.bullet_list:
            self.shadertoy.program['pos'] = bullet.position
            self.shadertoy.render()
        # self.bullet_list.draw()

    def on_key_press(self, key, modifiers):
        bullet = arcade.SpriteCircle(5, arcade.color.WHITE)
        bullet.center_x = 0
        bullet.center_y = self.height / 2
        bullet.change_x = 5
        self.bullet_list.append(bullet)

    def on_update(self, delta_time: float):
        self.bullet_list.update()


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
