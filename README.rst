Asteroids Smasher
=================

.. image:: screenshot.png
   :width: 50%

An asteroids clone made with the `Arcade library <https://api.arcade.academy>`_.

This example is designed to show off using shaders for visual effects.

.. list-table:: Project Files
   :widths: 25 75
   :header-rows: 1

   * - File
     - Description
   * - `__main__.py <blob/main/source/constants.py>`_
     - Bootstrap method that loads the fonts and starts the game.
   * - `asteroid_sprite.py <blob/main/source/asteroid_sprite>`_
     - Sprite that represents an asteroid.
   * - `bullet.py <blob/main/source/bullet>`_
     - Base class for all bullets/lasers shot by the players.
   * - `constants.py <blob/main/source/constants>`_
     - Holding place for all constants used in the program.
   * - `explosion.glsl <blob/main/source/explosion>`_
     - GLSL code used to display explosions.
   * - `explosion.py <blob/main/source/explosion>`_
     - Python code used to position and render the GLSL explosion code.
   * - `game_view.py <blob/main/source/game_view>`_
     - This is the main view that holds the game logic. If you are looking for the 'guts'
       of the game, this is it. If you aren't familiar with using "views" in Arcade, see the
       `View Tutorial <https://api.arcade.academy/en/latest/tutorials/views/index.html>`_.
   * - `glow_ball.glsl <blob/main/source/glow_ball>`_
     - GLSL code used to display a glowy-ball bullet.
   * - `glow_ball.py <blob/main/source/glow_ball>`_
     - Python code used to position and render the GLSL bullet code.
   * - `glow_image_sprite.py <blob/main/source/glow_image_sprite>`_
     - Python code used to position and render the GLSL bullet code.
   * - `glow_line.glsl <blob/main/source/glow_line>`_
     - GLSL code used to display a glowy-line laser/bullet.
   * - `glow_line.py <blob/main/source/glow_line>`_
     - Python code used to position and render the GLSL bullet code.
   * - ship_sprite.py
     - Space ship sprite to represent the player.
   * - `start_view.py <blob/main/source/start_view>`_
     - The starting screen that shows the instructions and allows the user to
       select number of players.
   * - `window.py <blob/main/source/window>`_
     - A subclass of Window that also tracks the joysticks that are plugged in.

