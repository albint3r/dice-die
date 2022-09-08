# Import
import pygame as pg
from pygame import mixer
import random
from config import config


class DiceView(pg.sprite.Sprite):
    DICE_IMG = {1: config.get('IMG').get('DICE1'),
                2: config.get('IMG').get('DICE2'),
                3: config.get('IMG').get('DICE3'),
                4: config.get('IMG').get('DICE4'),
                5: config.get('IMG').get('DICE5'),
                6: config.get('IMG').get('DICE6')}

    DICE_SIZE = (150, 150)
    TIME_SOUND_DELAY = 1500  # 0.5 seconds
    TIME_ROLLING = 560
    TIME_FLIP_DICE = 10

    def __init__(self, color: str, player_board):
        super().__init__()
        self.player = player_board
        self.color: str = color
        self.image = pg.transform.scale(pg.image.load(self.DICE_IMG.get(1)), self.DICE_SIZE)
        if self.color == 'Green':
            self.rect = self.image.get_rect(center=(1000, 770))
        if self.color == 'Red':
            self.rect = self.image.get_rect(center=(190, 230))
        self.animation_random_rolling_duration = self.TIME_FLIP_DICE  # is the time to the next dice img
        self.rolling_duration = self.TIME_ROLLING  # Is the time to throw the dice automatic
        self.random_rolling_sound = pg.mixer.Sound(config.get('SOUND').get('RANDOM_ROLLING'))
        self.roll_sound = pg.mixer.Sound(config.get('SOUND').get('THROW_DICE'))
        self.random_rolling_sound_flag = True  # If True the rolling dice will reproduce one time

    def roll_animation(self):
        """Create a Rollin animation when is the Turn of the player.
        This don't count like a dice throw this is only an animation.
        """

        # Is player turn?
        if self.player.is_turn:
            # He rolled the dice?
            if self.animation_random_rolling_duration <= 0 and not self.player.dice.number:
                random_number = random.randint(1, 6)
                # It selects a random image to create the rolling effect
                self.image = pg.transform.scale(pg.image.load(self.DICE_IMG.get(random_number)), self.DICE_SIZE)
                self.animation_random_rolling_duration = self.TIME_FLIP_DICE  # Reset Animation Duration
                if self.random_rolling_sound_flag:  # This play once the sound
                    self.random_rolling_sound.play()
                    self.random_rolling_sound_flag = False

            # Roll the dice if player time out
            if self.rolling_duration <= 0 and not self.player.dice.number:
                self.player.dice.roll()
                self.random_rolling_sound.stop()
                self.roll_sound.play()
                self.random_rolling_sound_flag = True  # Turn on this flag for the next turn apply the effect
                self.rolling_duration = self.TIME_ROLLING  # Reset Timer Random Rolling Sound effect
                self.animation_random_rolling_duration = self.TIME_FLIP_DICE  # Reset Animation Duration

            # Change the animation speed to create the next dice image
            if not self.player.dice.number:
                self.rolling_duration -= 5
                self.animation_random_rolling_duration -= 15

    def roll_dice(self):
        """Player Roll Dice when press space."""
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.player.is_turn and not self.player.dice.number:
            self.player.dice.roll()
            self.random_rolling_sound.stop()
            self.roll_sound.play()
            print(self.player.dice.number, self.player.player.name)
            self.random_rolling_sound_flag = True  # Turn on this flag for the next turn apply the effect
            self.rolling_duration = self.TIME_ROLLING  # Reset Timer Random Rolling Sound effect
            self.animation_random_rolling_duration = self.TIME_FLIP_DICE  # Reset Animation Duration

    def show_dice_result(self):
        """Show the real dice throw of the player in the boardgame"""
        if self.player.dice.number:
            self.image = pg.transform.scale(pg.image.load(self.DICE_IMG.get(self.player.dice.number)), self.DICE_SIZE)

    def update(self):
        self.roll_animation()
        self.roll_dice()
        self.show_dice_result()
