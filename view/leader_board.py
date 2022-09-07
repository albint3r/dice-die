# Imports
import pygame as pg


class LeaderBoardView:

    def __init__(self, score_match):
        self.screen = pg.display.get_surface()
        self.board_table = pg.sprite.GroupSingle(LeaderBoardTable(score_match))
        self.menu = None

    def run(self):
        self.board_table.draw(self.screen)
        self.board_table.update()


class LeaderBoardTable(pg.sprite.Sprite):
    IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\leader_board.png'
    FONT_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\font\Magical Story.ttf'
    SIZE = (1000, 800)

    def __init__(self, score_match):
        super(LeaderBoardTable, self).__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(pg.image.load(self.IMG_ROOT).convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=(600, 500))
        # Fonts
        self.font_title = pg.font.Font(self.FONT_ROOT, 100)
        self.font_board = pg.font.Font(self.FONT_ROOT, 40)
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
        height_spaces_players = 50  # The count start in 0
        for player in top_player:
            # Name
            name_surf = self.font_board.render(f'{player[0]}', False, 'White')
            name_rect = name_surf.get_rect(center=(300, y_pos + height_spaces_players))
            # Total Wins
            wins_surf = self.font_board.render(f'{player[1]}', False, 'White')
            wins_rect = wins_surf.get_rect(center=(600, y_pos + height_spaces_players))
            # Win rate
            win_rate_surf = self.font_board.render(f'{player[2]}', False, 'White')
            win_rate_rect = win_rate_surf.get_rect(center=(900, y_pos + height_spaces_players))
            # Display result
            self.screen.blit(name_surf, name_rect)
            self.screen.blit(wins_surf, wins_rect)
            self.screen.blit(win_rate_surf, win_rate_rect)
            # This adds space between the names
            y_pos = y_pos + height_spaces_players

    def update(self):
        self.show_top_player_stats()
        self.show_title_top_10()
