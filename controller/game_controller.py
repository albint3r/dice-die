# Import
import random

import pygame as pg
from pygame import mixer
import sys
# Model
from model.game_engine import GameModel
# Views
from view.score_bar import ScoreBarView
from view.board import BoarGameView
from view.dice import DiceView
from view.menu import MenuView
from view.winner_podium import WinnerPodiumView
from view.leader_board import LeaderBoardView
from view.how_to_play import HowToPlayView
from view.player_name_input import PlayerNameTextInput
# config
from config import config


class GameController:
    BACKGROUND_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\background_geo.png'

    def __init__(self):
        self.model: GameModel = GameModel()
        self.target_column: int | None = None  # This attribute will be used inside the  board view
        self.turn: int = 0  # p1 = 0 or p2 = 1
        self.screen_size: tuple[int, int] = (1200, 1000)
        self.FPS: int = 60
        self.active_game: bool = True
        self.game_state: dict = dict(menu=True, how_to_play=False, leader_board=False,
                                     match=False, player_input=False,
                                     winner=False, retry=False, retry_back=False)
        self.is_save: bool = True

        # Pygame
        pg.init()
        self.leader_board = None
        self.clock = None
        self.screen = None
        self.menu = None
        self.score_bar = None
        self.score_bar_group = None
        self.boars_group = None
        self.dice = None
        self.background_img = None
        self.background_rect = None
        self.winner_podium = None
        self.how_to_play = None
        self.player_text_input = None

    def create_new_game(self):
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.screen_size)
        # Menu
        self.menu = MenuView()
        # Leader board
        self.leader_board = LeaderBoardView(self.model.score_match)
        # Score Bar
        self.score_bar = ScoreBarView()  # Create Round corners
        self.score_bar_group = pg.sprite.GroupSingle(self.score_bar)
        self.score_bar.set_rounded()
        # Boards
        self.boars_group = pg.sprite.Group()
        self.boars_group.add(BoarGameView('Red', self.model.p1))
        self.boars_group.add(BoarGameView('Green', self.model.p2))
        # Dice
        self.dice = pg.sprite.Group()
        self.dice.add(DiceView('Red', self.model.p1))
        self.dice.add(DiceView('Green', self.model.p2))
        # Background
        self.background_img = pg.image.load(self.BACKGROUND_IMG)
        self.background_rect = self.background_img.get_rect(center=(600, 500))
        # Winner Podium
        self.winner_podium = WinnerPodiumView(self.model)
        # How to play
        self.how_to_play = HowToPlayView()
        # Player text input
        self.player_text_input = PlayerNameTextInput(self.model.p1, self.model.p2)

    def retry_game(self):
        p1_name = self.model.p1.player.name
        p2_name = self.model.p2.player.name
        self.turn = 0
        self.target_column = None
        self.model = GameModel()
        self.model.p1.player.name = p1_name
        self.model.p2.player.name = p2_name
        self.is_save = True  # This must be true to save the next match result
        self.select_game_state('match')
        self.create_new_game()

    def retry_back_game(self):
        """Create the game again but instead of replay the game it would send you to the main menu"""
        p1_name = self.model.p1.player.name
        p2_name = self.model.p2.player.name
        self.turn = 0
        self.target_column = None
        self.model = GameModel()
        self.model.p1.player.name = p1_name
        self.model.p2.player.name = p2_name
        self.is_save = True  # This must be true to save the next match result
        self.select_game_state('menu')
        self.create_new_game()

    def select_game_state(self, targe_state: str):
        """Select a target game state"""
        for state in self.game_state.keys():
            self.game_state[state] = False
        self.game_state[targe_state] = True

    def is_game_over(self, current_player):
        """Return True if the Game is Over.
        This method is revers that the method used in the Terminal object.
        In this case We expect False, to know the game is on.
        """
        if not self.model.is_game_over(current_player):
            self.select_game_state('winner')

    def play(self):
        # Create new game
        self.create_new_game()
        # Add Background game

        # Define which player starts first
        players = self.model.select_player_start()
        mixer.music.load(config.get('MUSIC').get(random.choice(['TRACK1', 'TRACK2'])))
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)
        while self.active_game:
            # Assign player turn and define opponent player in this turn
            current_player = players[self.turn]
            opponent = self.model.select_opponent(players, self.turn)

            # Roll the dice
            self.screen.fill('Black')  # To refresh the black screen
            self.screen.blit(self.background_img, self.background_rect)
            # Events
            for event in pg.event.get():
                # If player click cross exit game
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if self.game_state['menu']:
                    self.menu.create_new_dice(event)

            if self.game_state['menu']:
                self.menu.run(self.game_state)

            if self.game_state['how_to_play']:
                self.how_to_play.run(self.game_state)

            if self.game_state['leader_board']:
                self.leader_board.run(self.game_state)

            # Players had name?
            if self.game_state['player_input']:
                self.player_text_input.run(self.game_state)

            # If true Match in display
            if self.game_state['match']:
                # Dice
                self.dice.draw(self.screen)
                self.dice.update()

                # Score Bar
                self.score_bar.set_shadows()
                self.score_bar_group.draw(self.screen)
                self.score_bar_group.update(self.model.p1.points_board.total_points,
                                            self.model.p2.points_board.total_points,
                                            self.model.score_match.total_turns)

                # Boards
                self.boars_group.draw(self.screen)
                self.boars_group.update(
                    self.model.copy_fill_missing(self.model.p1.grid, reverse=True),
                    self.model.copy_fill_missing(self.model.p2.grid, reverse=False),
                    self.model.p1.points_board.points,
                    self.model.p2.points_board.points,
                    self.model.get_removed_dices_player(echo=False),
                    opponent,
                    self.model.score_match.plus_one_total_turn)  # Update turns

                # Is a Winner?
                self.is_game_over(current_player)
                # If not longer their player turn, activate change player turn.
                if not current_player.is_turn and self.game_state['match']:
                    self.turn = self.model.change_player_turn(self.turn)

            if self.game_state['winner']:
                self.model.select_winner()
                self.winner_podium.run(self.game_state, self.model.winner_status)
                if self.is_save:
                    # Save Game Match
                    self.model.fill_missing_dice_results(self.model.p1)
                    self.model.fill_missing_dice_results(self.model.p2)
                    self.model.save_game_result()
                    self.model.save_game_grid()
                    self.is_save = False  # Only this will be re-activated if the player retry the game

            if self.game_state['retry']:
                self.retry_game()
                players = self.model.select_player_start()

            if self.game_state['retry_back']:
                # This game state help to restart all the game settings and return the player
                # to the main menu instead of replay the game
                self.retry_back_game()
                players = self.model.select_player_start()

            # Update All Game
            pg.display.update()
            # Is Game Over or next player?
            self.clock.tick(self.FPS)
