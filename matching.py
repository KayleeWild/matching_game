""" Simple Matching arcade game
Kaylee Wright
10/2024
"""
# Imports:
import arcade
import random

import arcade.color

# Constants:
WIDTH = 800
HEIGHT = 600
TITLE = "Farm Matching"
BACKGROUND_COLOR = arcade.color.PAPAYA_WHIP
CARD_WIDTH = 100
CARD_HEIGHT = 100
SPACING = 10
ROWS = 4
COLUMNS = 4
PAIRS_AMOUNT = 8


# Classes
class Matching(arcade.Window):
    """ Classic matching game. 
    Window is populated with a grid of face-down cards.
    User takes turns flipping cards two at a time. If they match, 
    the cards stay face-up. If they don't, cards are returned to face down
    and play continues. Game ends when the player has found all the matches
    and all cards are face up.
    """
    def __init__(self, width, height, title):
        # Initialize game
        super().__init__(width, height, title)
        # Set up empty sprite lists
        self.cards_list = arcade.SpriteList()
        self.last_clicked = None
        self.flipped_1 = None
        self.flipped_2 = None
        self.fronts_list = ["images/50pxfarmer.png"
                       , "images/50pxCorn.png"
                       , "images/25pxhopper.png"
                       , "images/barn.png"
                       , "images/combine.png"
                       , "images/crops.png"
                       , "images/rake.png"
                       , "images/tractor.png"]
    
    def setup(self):
        # Starting up game
        arcade.set_background_color(BACKGROUND_COLOR)
        # Sounds
        self.match_sound = arcade.load_sound(":resources:sounds/coin5.wav")
        # create the cards by value
        value_list = list(range(1, PAIRS_AMOUNT + 1)) * 2
        # shuffle the card values in the list
        random.shuffle(value_list)
        # Iterate through the values list and make a new card with needed attributes for each one
        for value in value_list:
            # Create a card with the back image
            card = arcade.Sprite("images/100pxcard_back.jpg")
            # Give it some attributes
            card.value = value
            card.is_flipped = False
            card.front = self.fronts_list[value - 1]
            # Add it to the sprite list
            self.cards_list.append(card)
        # Iterate through the grid placements to put cards in the window 
        start_x = (WIDTH - ((COLUMNS * CARD_WIDTH) + ((COLUMNS - 1) * SPACING))) / 2
        start_y = (HEIGHT + ((ROWS * CARD_HEIGHT) + ((ROWS - 1) * SPACING))) / 2
        for i, card in enumerate(self.cards_list):
            row = i // COLUMNS
            col = i % COLUMNS

            card.center_x = start_x + col * ((CARD_WIDTH + SPACING))
            card.center_y = start_y - row * ((CARD_HEIGHT + SPACING))

    def on_mouse_press(self, x, y, button, modifiers):
        # define card that was clicked
        clicked_list = arcade.get_sprites_at_point((x, y), self.cards_list)
        # exit function if the card is already flipped, or if area clicked wasn't a card
        if not clicked_list:
            return
        clicked = clicked_list[0]
        if clicked.is_flipped == True:
            return
        # if not, flip the card over
        clicked.texture = arcade.load_texture(clicked.front)
        clicked.is_flipped = True
        # check that card is first to be flipped
        if self.last_clicked != None:
            # if card is second to be flipped, check for match
            if clicked.value == self.last_clicked.value: # match!!
                arcade.play_sound(self.match_sound)
                self.last_clicked = None
                return
            elif clicked.value != self.last_clicked.value and self.last_clicked != None: # No match
                self.flipped_1 = clicked
                self.flipped_2 = self.last_clicked
                arcade.schedule(self.flip_to_back, 1.0)
                self.last_clicked = None
                return
        else:
            self.last_clicked = clicked

    def flip_to_back(self, delta_time):
        self.flipped_1.texture = arcade.load_texture("images/100pxcard_back.jpg")
        self.flipped_1.is_flipped = False
        self.flipped_2.texture = arcade.load_texture("images/100pxcard_back.jpg")
        self.flipped_2.is_flipped = False
        arcade.unschedule(self.flip_to_back)
            
    def on_draw(self):
        arcade.start_render()
        self.cards_list.draw()

if __name__ == "__main__":
    game = Matching(WIDTH, HEIGHT, TITLE)
    game.setup()
    arcade.run()
    
        

    