# Import
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


class GameController:
    BACKGROUND_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\background_geo.png'

    def __init__(self):
        self.model: GameModel = GameModel()
        self.target_column: int | None = None  # This attribute will be used inside the  board view
        self.turn: int = 0  # p1 = 0 or p2 = 1
        self.screen_size: tuple[int, int] = (1200, 1000)
        self.FPS: int = 60
        self.active_game: bool = True
        self.game_state: dict = dict(menu=True, how_to_play=False,
                                     leader_board=False, match=False,
                                     winner=False, retry=False)

        # Pygame
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(self.screen_size)
        # Menu
        self.menu = MenuView()
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

    def is_game_over(self, current_player):
        """Return True if the Game is Over.
        This method is revers that the method used in the Terminal object.
        In this case We expect False, to know the game is on.
        """
        if not self.model.is_game_over(current_player):
            self.game_state['menu'] = False
            self.game_state['match'] = False
            self.game_state['how_to_play'] = False
            self.game_state['leader_board'] = False
            self.game_state['winner'] = True  # <-----------

    def play(self):
        # Show leader board before start the game

        # Add Background game

        # Define which player starts first
        players = self.model.select_player_start()
        mixer.music.load(r'C:\Users\albin\PycharmProjects\dice_&_die\statics\music\libella_swing.mp3')
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)
        while self.active_game:
            # Assign player turn and define opponent player in this turn
            current_player = players[self.turn]
            opponent = self.model.select_opponent(players, self.turn)

            # print(current_player.grid)
            # Roll the dice

            self.screen.fill('Black')  # To refresh the black screen
            self.screen.blit(self.background_img, self.background_rect)
            for event in pg.event.get():
                # If player click cross exit game
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if self.game_state['menu']:
                    self.menu.create_new_dice(event)

            if self.game_state['menu']:
                self.menu.run(self.game_state)

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
                # self.model.winner_status = 0
                self.winner_podium.run(self.game_state, self.model.winner_status)

            if self.game_state['retry']:
                print('que ondaaa!')
                # p1_name = self.model.p1.player.name
                # p2_name = self.model.p2.player.name
                # self.turn = 0
                # self.target_column = None
                # self.model = GameModel()
                # self.model.p1.player.name = p1_name
                # self.model.p2.player.name = p2_name
                # self.game_state['menu'] = False
                # self.game_state['match'] = True  # <----------
                # self.game_state['how_to_play'] = False
                # self.game_state['leader_board'] = False
                # self.game_state['winner'] = False
                # self.game_state['retry'] = False

            # Update All Game
            pg.display.update()
            # Is Game Over or next player?
            self.clock.tick(self.FPS)

        # Save Game Match
        self.model.fill_missing_dice_results(self.model.p1)
        self.model.fill_missing_dice_results(self.model.p2)
        self.model.save_game_result()
        self.model.save_game_grid()
