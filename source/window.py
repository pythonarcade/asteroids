import arcade


class Window(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.joysticks = arcade.get_joysticks()

        for joystick in self.joysticks:
            joystick.open()
