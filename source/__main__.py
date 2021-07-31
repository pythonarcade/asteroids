import arcade
from constants import *
from game_view import GameView


def main():
    """ Start the game """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()
