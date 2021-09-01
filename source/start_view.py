import arcade
from game_view import GameView


class StartView(arcade.View):
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        line_height = 70
        line_location = self.window.height - line_height * 2
        arcade.draw_text("Asteroid Smasher",
                         self.window.width / 2,
                         line_location,
                         arcade.color.WHITE,
                         font_size=50,
                         anchor_x="center",
                         font_name="SF Atarian System")

        line_location -= line_height
        line_location -= line_height

        arcade.draw_text("1 - Start One Player Game",
                         self.window.width / 2,
                         line_location,
                         arcade.color.WHITE,
                         font_size=40,
                         anchor_x="center",
                         font_name="SF Atarian System")

        if len(self.window.joysticks) > 1:
            color = arcade.color.WHITE
        else:
            color = arcade.color.GRAY

        line_location -= line_height

        arcade.draw_text("2 - Start Two Player Game",
                         self.window.width / 2,
                         line_location,
                         color,
                         font_size=40,
                         anchor_x="center",
                         font_name="SF Atarian System")

        line_location -= line_height
        line_location -= line_height
        color = arcade.color.WHITE

        arcade.draw_text("Use joysticks to play, or arrow keys to move and number keys to fire.",
                         self.window.width / 2,
                         line_location,
                         color,
                         font_size=40,
                         anchor_x="center",
                         font_name="SF Atarian System")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1:
            game_view = GameView()
            game_view.start_new_game(1)
            self.window.show_view(game_view)
        elif symbol == arcade.key.KEY_2:
            game_view = GameView()
            game_view.start_new_game(2)
            self.window.show_view(game_view)
