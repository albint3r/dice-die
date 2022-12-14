# Imports
import pygame as pg
# Modules Projects
from view.menu import ButtonView
from config import config


class LeaderBoardView:

    def __init__(self, score_match):
        self.screen = pg.display.get_surface()
        self.board_table = pg.sprite.GroupSingle(LeaderBoardTable(score_match))
        self.menu = pg.sprite.Group()
        self.menu.add(ButtonView(600, 920, 'Back to menu'))

    def run(self, game_state):
        # Menu
        self.menu.draw(self.screen)
        self.menu.update(game_state)
        # Board
        self.board_table.draw(self.screen)
        self.board_table.update()


class LeaderBoardTable(pg.sprite.Sprite):
    SIZE = (1000, 800)

    def __init__(self, score_match):
        super(LeaderBoardTable, self).__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(pg.image.load(config.get('IMG').get('LEADER_BOARD')).convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=(600, 500))
        # Fonts
        self.font_title = pg.font.Font(config.get('FONT').get('MAGIC'), 100)
        self.font_board = pg.font.Font(config.get('FONT').get('MAGIC'), 40)
        # SQL Table
        self.score_match = score_match

    def show_title_top_10(self):
        """Show the main title in the menu"""
        title = self.font_title.render('Top 10 Players', False, 'Black')
        title_rect = title.get_rect(center=(600, 100))
        self.screen.blit(title, title_rect)

    def show_top_player_stats(self):
        """Display the name of the top players"""
        top_player = self.score_match.get_leader_score()
        y_pos = 280
        height_spaces_players = 50  # The count start in 03
        for player in top_player:
            # Name
            name_surf = self.font_board.render(f'{player[0]}', False, 'White')
            name_rect = name_surf.get_rect(center=(300, y_pos + height_spaces_players))
            # Total Wins
            wins_surf = self.font_board.render(f'{player[1]}', False, 'White')
            wins_rect = wins_surf.get_rect(center=(600, y_pos + height_spaces_players))
            # Win rate
            avg_turn_surf = self.font_board.render(f'{player[2]:.0f}', False, 'White')
            avg_turns_rect = avg_turn_surf.get_rect(center=(900, y_pos + height_spaces_players))
            # Display result
            self.screen.blit(name_surf, name_rect)
            self.screen.blit(wins_surf, wins_rect)
            self.screen.blit(avg_turn_surf, avg_turns_rect)
            # This adds space between the names
            y_pos = y_pos + height_spaces_players

    def show_table_labels(self):
        """Display the name of the top players"""

        labels = ('Name', 'Total Wins', 'Avg. Turns to win')
        x_pos = (300, 600, 900)

        for x, label in zip(x_pos, labels):
            # label
            label = self.font_board.render(label, False, 'White')
            label_rect = label.get_rect(center=(x, 250))
            self.screen.blit(label, label_rect)

    def update(self):
        self.show_table_labels()
        self.show_top_player_stats()
        self.show_title_top_10()
