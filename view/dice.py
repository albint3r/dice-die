# Import
import pygame as pg
from pygame import mixer
import random


class DiceView(pg.sprite.Sprite):
    DICE_IMG = {1: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\1.png',
                2: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\2.png',
                3: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\3.png',
                4: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\4.png',
                5: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\5.png',
                6: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\6.png'}

    RANDOM_ROLLING_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\sound\dice_random_rolling_effect.mp3'
    DICE_ROLL_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\sound\dice_roll.mp3'
    DICE_SIZE = (150, 150)
    TIME_SOUND_DELAY = 1500  # 0.5 seconds

    def __init__(self, color: str, player_board):
        super().__init__()
        self.player = player_board
        self.color: str = color
        self.image = pg.transform.scale(pg.image.load(self.DICE_IMG.get(1)), self.DICE_SIZE)
        if self.color == 'Green':
            self.rect = self.image.get_rect(center=(1000, 770))
        if self.color == 'Red':
            self.rect = self.image.get_rect(center=(190, 230))
        self.animation_random_rolling_duration = 60
        self.rolling_duration = 900  # seconds max
        self.random_rolling_sound = pg.mixer.Sound(self.RANDOM_ROLLING_ROOT)
        self.roll_sound = pg.mixer.Sound(self.DICE_ROLL_ROOT)
        self.random_rolling_sound_flag = True

    def roll_animation(self):
        """Create a Rollin animation when is the Turn of the player.
        This don't count like a dice throw this is only an animation.
        """


        # Is player turn?
        if self.player.is_turn:
            random_number = random.randint(1, 6)
            # He rolled the dice?
            if self.animation_random_rolling_duration <= 0 and not self.player.dice.number:
                # This logic help to only play once the dice rolling effect
                if self.random_rolling_sound_flag:
                    self.random_rolling_sound.play()
                    self.random_rolling_sound_flag = False
                # It selects a random image to create the rolling effect
                self.image = pg.transform.scale(pg.image.load(self.DICE_IMG.get(random_number)), self.DICE_SIZE)
                # After change the dice image actualize the initial animation speed for the next dice display
                self.animation_random_rolling_duration = 60
            # Change the animation speed to create the next dice image
            self.animation_random_rolling_duration -= 15

            if not self.player.dice.number:  # TODO look the way to refactorings this method
                self.rolling_duration -= 5

            # Roll the dice if player time out
            if self.rolling_duration <= 0 and not self.player.dice.number and self.player:
                self.player.dice.roll()
                self.random_rolling_sound.stop()
                self.roll_sound.play()
                print(f'Resultado {self.player.dice.number}', self.player.player.name)
                self.random_rolling_sound_flag = True  # Turn on this flag for the next turn apply the effect
                self.rolling_duration = 900  # Reset Timer Random Rolling Sound effect

    def roll_dice(self):
        """Player Roll Dice when press space."""
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.player.is_turn and not self.player.dice.number:
            self.player.dice.roll()
            self.random_rolling_sound.stop()
            self.roll_sound.play()
            print(self.player.dice.number, self.player.player.name)
            self.random_rolling_sound_flag = True
            self.rolling_duration = 900  # Reset Timer Random Rolling Sound effect

    def show_dice_result(self):
        if self.player.dice.number:
            self.image = pg.transform.scale(pg.image.load(self.DICE_IMG.get(self.player.dice.number)), self.DICE_SIZE)

    def update(self):
        self.roll_animation()
        self.roll_dice()
        self.show_dice_result()
