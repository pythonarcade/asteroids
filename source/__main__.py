import arcade
from constants import *
from start_view import StartView
from window import Window


def main():
    """ Start the game """

    # Load fonts
    arcade.load_font("../fonts/arcade.ttf")
    arcade.load_font("../fonts/SF Atarian System.ttf")

    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
