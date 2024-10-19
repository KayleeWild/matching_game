# Basic arcade shooter
# Adapted from Real Python Tutorial @ https://realpython.com/arcade-python-game-framework/ 

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Farm Shooter"
SCALING = 2.0
SCORE = 0
LIVES = 5
SCORE_LOOP = 0

# Classes
class FlyingSprite(arcade.Sprite):
    """Base class for clouds and enemies
    """
    def update(self):
        """Update sprite position
        When moves off screen, remove it
        """
        # Move sprite
        super().update()
        # Remove if off screen
        if self.right < 0:
            self.remove_from_sprite_lists()

class FarmShooter(arcade.Window):
    """Farm Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """
    def __init__(self, width: int, height: int, title: str):
        # initialize the game
        super().__init__(width, height, title)
        # set up empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.corns_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        """Getting the game ready 
        """
        # Background color
        arcade.set_background_color(arcade.color.CHAMOISEE)
        # Score setup
        self.score = SCORE
        self.lives = LIVES
        self.score_loop = SCORE_LOOP
        # player setup
        self.player = arcade.Sprite("images/50pxfarmer.png", SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)
        # Spawn new enemy every 1/4 second
        arcade.schedule(self.add_enemy, 0.25)
        # Spawn new could every second
        arcade.schedule(self.add_corn, 1.0)
        # Sound stuff
        self.corn_sound = arcade.load_sound(":resources:sounds/coin5.wav")
        self.enemy_sound = arcade.load_sound(":resources:sounds/error5.wav")
        # Presets
        self.paused = False

    def add_enemy(self, delta_time: float):
        """Adds new enemy on screen
        Arguments:
            delta_time {float} -- How much time passed since last call
        """
        # Create new sprite
        enemy = FlyingSprite("images/25pxHopper.png", SCALING)
        # Set position
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)
        # Set speed (random heading left)
        enemy.velocity = (random.randint(-10, -5), 0)
        # Add to enemy list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_corn(self, delta_time: float):
        """Adds new corn
        Arguments:
            delta_time {float} -- How much time passed since last call
        """
        # Create new sprite
        corn = FlyingSprite("images/50pxCorn.png", SCALING)
        # Set position
        corn.left = random.randint(self.width, self.width + 80)
        corn.top = random.randint(10, self.height - 10)
        # Set speed (random heading left)
        corn.velocity = (random.randint(-5, -2), 0)
        # Add to corns list
        self.corns_list.append(corn)
        self.all_sprites.append(corn)

    def on_key_press(self, symbol, modifiers):
        """Handle keyboard input
        Q: quit the game
        P: Pause/unpause the game
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguements:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            arcade.close_window()
        if symbol == arcade.key.P:
            self.paused = not self.paused
        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 5
        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -5
        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -5
        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 5

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released
        Arguememts:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0
        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.RIGHT
            or symbol == arcade.key.LEFT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        """Update positions of everything, pause if paused
        Arguements:
            delta_time {float} -- Time since last update
        """
        # exit if paused
        if self.paused:
            return
        # Lose life if hit anything
        enemy_collisions = arcade.check_for_collision_with_list(self.player, self.enemies_list)
        for enemy in enemy_collisions:
            self.lives -= 1
            enemy.kill()
            arcade.play_sound(self.enemy_sound)
        # End game if lives < 0
        if self.lives == 0:
            arcade.close_window()
        # Add score if hits corn
        corn_collisions = arcade.check_for_collision_with_list(self.player, self.corns_list)
        for corn in corn_collisions:
            self.score += 100
            self.score_loop += 100
            corn.kill()
            arcade.play_sound(self.corn_sound)
            if self.score_loop >= 1000:
                self.lives += 1
                self.score_loop = 0

        # update everything
        self.all_sprites.update()
        # Keep player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        """Draw all game objects
        """
        arcade.start_render()
        self.all_sprites.draw()
        arcade.draw_text(f"Score: {self.score}", 10, self.height - 50, arcade.color.BLACK_BEAN, 20, font_name="Kenney Pixel Square")
        arcade.draw_text(f"Lives: {self.lives}", 10, self.height - 100, arcade.color.BLACK_BEAN, 20, font_name="Kenney Pixel Square")

if __name__ == "__main__":
    farm_game = FarmShooter(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    farm_game.setup()
    arcade.run()