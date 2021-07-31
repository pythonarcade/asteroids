import random
import math
import arcade


from typing import cast
from arcade.experimental.shadertoy import Shadertoy

from constants import *
from asteroid_sprite import AsteroidSprite
from ship_sprite import ShipSprite
from bullet import Bullet
from glow_line import GlowLine
from glow_ball import GlowBall
from explosion import ExplosionMaker
from glow_image_sprite import GlowImageSprite


class GameView(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()

        self.game_over = False

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.lives = 3

        # Sounds
        self.laser_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound1 = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.hit_sound2 = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.hit_sound3 = arcade.load_sound(":resources:sounds/hit1.wav")
        self.hit_sound4 = arcade.load_sound(":resources:sounds/hit2.wav")

        self.glowball_shadertoy = Shadertoy.create_from_file(self.window.get_size(), "glow_ball.glsl")
        self.glowline_shadertoy = Shadertoy.create_from_file(self.window.get_size(), "glow_line.glsl")

        self.explosion_list = []

    def start_new_game(self):
        """ Set up the game and initialize the variables. """

        self.game_over = False
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        # Set up the player
        self.score = 0

        if len(self.window.joysticks) > 0:
            joystick = self.window.joysticks[0]
        else:
            joystick = None
        self.player_sprite = ShipSprite(":resources:images/space_shooter/playerShip1_orange.png",
                                        SCALE,
                                        joystick)
        self.player_sprite_list.append(self.player_sprite)
        self.lives = 3

        # Set up the little icons that represent the player lives.
        cur_pos = 10
        for i in range(self.lives):
            life = arcade.Sprite(":resources:images/space_shooter/playerLife1_orange.png", SCALE)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.ship_life_list.append(life)

        # Make the asteroids
        image_list = (":resources:images/space_shooter/meteorGrey_big1.png",
                      ":resources:images/space_shooter/meteorGrey_big2.png",
                      ":resources:images/space_shooter/meteorGrey_big3.png",
                      ":resources:images/space_shooter/meteorGrey_big4.png")
        for i in range(STARTING_ASTEROID_COUNT):
            image_no = random.randrange(4)
            enemy_sprite = AsteroidSprite(image_list[image_no], SCALE)
            enemy_sprite.guid = "Asteroid"

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1

            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.asteroid_list.append(enemy_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.asteroid_list.draw()
        self.ship_life_list.draw()

        for bullet in self.bullet_list:
            bullet.draw()

        self.bullet_list.draw()
        for explosion in self.explosion_list:
            explosion.render()

        self.player_sprite_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 80, arcade.color.AMBER,
                         font_size=35,
                         font_name="Arcade")

        output = f"Asteroid Count: {len(self.asteroid_list)}"
        arcade.draw_text(output, 10, 40, arcade.color.AMBER,
                         font_size=35,
                         font_name="Arcade")

    def on_key_press(self, symbol, modifiers):
        """ Called whenever a key is pressed. """
        # Shoot if the player hit the space bar and we aren't respawning.
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0.15
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = -.2
        elif symbol == arcade.key.KEY_1:
            color = (255, 128, 128)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_2:
            color = (128, 255, 128)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_3:
            color = (128, 128, 255)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_4:
            color = (255, 128, 255)
            self.fire_circle(color)
        elif symbol == arcade.key.KEY_5:
            color = (255, 255, 255)
            self.fire_line(color)
        elif symbol == arcade.key.KEY_6:
            color = (64, 255, 64)
            self.fire_line(color)
        elif symbol == arcade.key.KEY_7:
            bullet_sprite = GlowImageSprite(":resources:images/space_shooter/laserBlue01.png",
                                            SCALE,
                                            glowcolor=arcade.color.WHITE,
                                            shadertoy=self.glowball_shadertoy)
            self.set_bullet_vector(bullet_sprite, 13)
            arcade.play_sound(self.laser_sound)

        elif symbol == arcade.key.E:
            explosion = ExplosionMaker(self.get_size(), self.player_sprite.position)
            self.explosion_list.append(explosion)

    def fire_circle(self, bullet_color):
        bullet_sprite = GlowBall(glowcolor=bullet_color, radius=5, shadertoy=self.glowball_shadertoy)
        self.set_bullet_vector(bullet_sprite, 5)
        arcade.play_sound(self.laser_sound)

    def fire_line(self, bullet_color):
        bullet_sprite = GlowLine(glowcolor=bullet_color, shadertoy=self.glowline_shadertoy, player=self.player_sprite)
        self.set_bullet_vector(bullet_sprite, 13)
        arcade.play_sound(self.laser_sound)

    def set_bullet_vector(self, bullet_sprite, bullet_speed):
        bullet_sprite.change_y = \
            math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
        bullet_sprite.change_x = \
            -math.sin(math.radians(self.player_sprite.angle)) \
            * bullet_speed

        bullet_sprite.center_x = self.player_sprite.center_x
        bullet_sprite.center_y = self.player_sprite.center_y

        self.bullet_list.append(bullet_sprite)

    def on_key_release(self, symbol, modifiers):
        """ Called whenever a key is released. """
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = 0

    def split_asteroid(self, asteroid: AsteroidSprite):
        """ Split an asteroid into chunks. """
        x = asteroid.center_x
        y = asteroid.center_y
        self.score += 1

        if asteroid.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                              ":resources:images/space_shooter/meteorGrey_med2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound1.play()

        elif asteroid.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_small1.png",
                              ":resources:images/space_shooter/meteorGrey_small2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound2.play()

        elif asteroid.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_tiny1.png",
                              ":resources:images/space_shooter/meteorGrey_tiny2.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.asteroid_list.append(enemy_sprite)
                self.hit_sound3.play()

        elif asteroid.size == 1:
            self.hit_sound4.play()

    def on_update(self, x):
        """ Move everything """

        if not self.game_over:
            self.asteroid_list.update()
            self.bullet_list.update()
            self.player_sprite_list.update()
            explosion_list_copy = self.explosion_list.copy()
            for explosion in explosion_list_copy:
                explosion.update(x)
                if explosion.time > .9:
                    self.explosion_list.remove(explosion)

            for bullet in self.bullet_list:
                asteroids = arcade.check_for_collision_with_list(bullet, self.asteroid_list)

                if len(asteroids) > 0:
                    explosion = ExplosionMaker(self.window.get_size(), bullet.position)
                    self.explosion_list.append(explosion)

                for asteroid in asteroids:
                    # explosion = ExplosionMaker(self.get_size(), bullet.position)
                    # self.explosion_list.append(explosion)

                    self.split_asteroid(cast(AsteroidSprite, asteroid))  # expected AsteroidSprite, got Sprite instead
                    asteroid.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()

                # Remove bullet if it goes off-screen
                size = max(bullet.width, bullet.height)
                if bullet.center_x < 0 - size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_x > SCREEN_WIDTH + size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y < 0 - size:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y > SCREEN_HEIGHT + size:
                    bullet.remove_from_sprite_lists()

            if not self.player_sprite.respawning:
                asteroids = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
                if len(asteroids) > 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        self.split_asteroid(cast(AsteroidSprite, asteroids[0]))
                        asteroids[0].remove_from_sprite_lists()
                        self.ship_life_list.pop().remove_from_sprite_lists()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")
