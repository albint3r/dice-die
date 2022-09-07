# Import
import pygame as pg
# Project Modules
from view.menu import ButtonView


class WinnerPodiumView:
    FONT_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\font\Magical Story.ttf'

    def __init__(self, model):
        self.screen = pg.display.get_surface()
        self.model = model
        self.winner = None
        self.loser = None
        self.winner_score = None
        self.loser_score = None
        self.is_tie = False
        # Trophy
        self.trophy = pg.sprite.GroupSingle(Trophy(600, 200))
        self.font = pg.font.Font(self.FONT_ROOT, 80)
        # Buttons
        self.menu = pg.sprite.Group()
        self.menu.add(ButtonView(400, 910, 'retry'))
        self.menu.add(ButtonView(800, 910, 'back to menu'))

    def set_player_places(self, winner_status):
        """Set the players places on the match"""
        if winner_status == 0 and self.winner is None:  # Player 1 win
            self.winner = self.model.p1
            self.loser = self.model.p2
        if winner_status == 1 and self.winner is None:  # Player 2 win
            self.winner = self.model.p2
            self.loser = self.model.p1
        if winner_status == 2 and self.winner is None:  # Tie
            self.winner = self.model.p1
            self.loser = self.model.p2
            self.is_tie = True

    def set_game_result(self):
        """Set the points of the winner and the loser to display the result"""
        if self.winner_score is None and self.loser_score is None:
            self.winner_score = self.winner.points_board.total_points
            self.loser_score = self.loser.points_board.total_points

    def show_player_game_score(self):
        # Winner
        winner_points = self.font.render(f'{self.winner_score}', False, 'Black')
        winner_points_rect = winner_points.get_rect(center=(300, 200))
        # Loser
        loser_points = self.font.render(f'{self.loser_score}', False, 'Black')
        loser_points_rect = loser_points.get_rect(center=(900, 200))
        # Show
        self.screen.blit(winner_points, winner_points_rect)
        self.screen.blit(loser_points, loser_points_rect)

    def show_player_game_names(self):
        # Winner
        winner_name = self.font.render(f'{self.winner.player.name}', False, 'Black')
        winner_name_rect = winner_name.get_rect(center=(300, 280))
        # Loser
        loser_name = self.font.render(f'{self.loser.player.name}', False, 'Black')
        loser_name_rect = loser_name.get_rect(center=(900, 280))
        # Show
        self.screen.blit(winner_name, winner_name_rect)
        self.screen.blit(loser_name, loser_name_rect)

    def show_player_winner_name_in_trophy(self):
        # Winner
        font = pg.font.Font(self.FONT_ROOT, 25)
        if not self.is_tie:
            winner_name = font.render(f'{self.winner.player.name}', False, 'Black')
        else:
            winner_name = font.render(f'NO WINNER', False, 'Black')
        winner_name_rect = winner_name.get_rect(center=(600, 345))
        # Show
        self.screen.blit(winner_name, winner_name_rect)

    def run(self, game_state,  winner_status):
        """Run all the methods and functions of all the objects"""

        self.trophy.draw(self.screen)
        self.set_player_places(winner_status)
        self.set_game_result()
        self.show_player_game_score()
        self.show_player_game_names()
        self.show_player_winner_name_in_trophy()
        # Menu
        self.menu.draw(self.screen)
        self.menu.update(game_state)


class Trophy(pg.sprite.Sprite):
    IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\trophy.png'
    SIZE = (300, 400)

    def __init__(self, x_pos, y_pos):
        super(Trophy, self).__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(pg.image.load(self.IMG_ROOT).convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x = x_pos
        self.y = y_pos
