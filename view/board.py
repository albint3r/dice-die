# Import
import pygame as pg
# Model
from model.game_engine import GameModel


class BoarGameView(pg.sprite.Sprite):
    RED_BOARD_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\red_board.png'
    GREEN_BOARD_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\green_board.png'
    SLASH_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\slash1.png'
    # FONT_ROOT = r'../statics/font/Magical Story.ttf'
    FONT_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\font\Magical Story.ttf'
    BOARDS_SIZE = (600, 400)
    COL_SIZE = (163, 247)

    def __init__(self, board_color: str, player_board):
        super().__init__()
        self.color = board_color
        self.player = player_board
        self.font = pg.font.Font(self.FONT_ROOT, 60)
        self.font_points = pg.font.Font(self.FONT_ROOT, 40)
        self.target_column: int | None = None

        if self.color == 'Red':
            self.x, self.y = (600, 250)
            self.image = pg.transform.scale(pg.image.load(self.RED_BOARD_IMG_ROOT).convert_alpha(), self.BOARDS_SIZE)
            self.rect = self.image.get_rect(center=(self.x, self.y))
            # Col coordinates
            self.col1_coor = ((430, 200), (430, 285), (430, 375))
            self.col2_coor = ((600, 200), (600, 285), (600, 375))
            self.col3_coor = ((770, 200), (770, 285), (770, 375))

        if self.color == 'Green':
            self.x, self.y = (600, 750)
            self.image = pg.transform.scale(pg.image.load(self.GREEN_BOARD_IMG_ROOT).convert_alpha(), self.BOARDS_SIZE)
            self.rect = self.image.get_rect(center=(self.x, self.y))
            # Col coordinates
            self.col1_coor = ((430, 635), (430, 725), (430, 810))
            self.col2_coor = ((600, 635), (600, 725), (600, 810))
            self.col3_coor = ((770, 635), (770, 725), (770, 810))

        # Grid Invisible Blocks
        self.grid_rects: dict = dict()
        self.grid_main: dict | None = None
        self.grid_points: dict | None = None
        self.col_image = pg.Surface(self.COL_SIZE)
        self.slash_flag = 15  # 60 FPS X SEG = 3 SEG
        self.removed_events: dict | None = None  # is a list that contain boolean indicators to remove dices

    def assign_grid_to_board_color(self, grid_p1, grid_p2):
        """Assign the Grid Board of the player depends on the color"""
        if self.color == 'Red':
            self.grid_main = grid_p1
        if self.color == 'Green':
            self.grid_main = grid_p2

    def assign_points_to_board_color(self, points_p1, points_p2):
        """Assign the Grid Board of the player depends on the color"""
        if self.color == 'Red':
            self.grid_points = points_p1
        if self.color == 'Green':
            self.grid_points = points_p2

    def assign_removed_events(self, removed_dices_player) -> None:
        """Assign the removed dice evento to each board depends on the color
        This helps to identify where would be printed a X mark when a dice is destroyed
        """
        for player, events in removed_dices_player.items():
            if self.color == 'Red' and player == 1:
                self.removed_events = events
            if self.color == 'Green' and player == 2:
                self.removed_events = events

    def proces_removed_events(self):
        """This method would activate the removed dice animation effect on the player board."""
        for col, event in self.removed_events.items():
            if event:
                # TODO BY THE MOMENT THIS ONLY IDENTIFY THE ROW AN THE PLAYER BOARD EVENT
                # I need to proces the action and set a timer duration
                # print(self.color, self.removed_events)
                pass
            # print(self.color, self.removed_events)

    def set_grid_rects(self, screen, show: bool = False):
        """Set grid Rectangles By there type of color.
        This helps to detect better the click collision to select the dice position.
        """
        if self.color == 'Red':
            coordinates = ((354, 154), (520, 154), (682, 154))
            self.grid_rects = {i: self.col_image.get_rect(topleft=coordinate) for i, coordinate in
                               enumerate(coordinates)}

        if self.color == 'Green':
            coordinates = ((354, 592), (520, 592), (682, 592))
            self.grid_rects = {i: self.col_image.get_rect(topleft=coordinate) for i, coordinate in
                               enumerate(coordinates)}

        if show:
            for key, val in self.grid_rects.items():
                pg.draw.rect(screen, 'White', val)

    def set_grid_numbers(self, screen, grid: dict[list, list, list]) -> None:
        """Display the Numbers on the grid by there type of color

        Parameters:
        ------------
        screen:
        grid: dict[list, list, list]:
            Is the Grid object from the Boar Object. This will be a copy of the original.
            Because it must have a transformation using the fill_na method. That help
            to fill the missing spaces with 0.
            If is not zero in the grid passing to this method it would have error.
        """

        if self.color == 'Red':
            col_coordinates_list = (self.col1_coor, self.col2_coor, self.col3_coor)
            self.validate_and_show_grid_numbers(screen, col_coordinates_list, grid)

        if self.color == 'Green':
            col_coordinates_list = (self.col1_coor, self.col2_coor, self.col3_coor)
            self.validate_and_show_grid_numbers(screen, col_coordinates_list, grid)

    def set_grid_points(self, screen, grid_point: dict):
        """Validate the Board Color Player and Display it the Points Score of each player."""
        if self.color == 'Red':
            col_coordinates_lst = (430, 135), (600, 135), (770, 135)

        if self.color == 'Green':
            col_coordinates_lst = (430, 870), (600, 870), (770, 870)

        for i, col in enumerate(col_coordinates_lst, start=1):
            text = self.font_points.render(f'{grid_point[i]}', False, 'Black')
            text_rect = text.get_rect(center=col)
            screen.blit(text, text_rect)

    def show_slash(self, screen, x: int, y: int):

        if not self.slash_flag <= 0:
            slash_img = pg.transform.scale(pg.image.load(self.SLASH_IMG).convert_alpha(), (500, 500))
            slash_img_rect = slash_img.get_rect(center=(x, y))
            screen.blit(slash_img, slash_img_rect)
            self.slash_flag -= 1

    def validate_and_show_grid_numbers(self, screen, col_coordinates_list: tuple, grid: dict[list, list, list]):
        """Validate if the Column of the grid have values and display it.
        This method assume that the grid was prepared with the copy and fill method of the Game engine class.
        """
        for i, col_cor in enumerate(col_coordinates_list, start=1):
            for ii, coordinate in enumerate(col_cor):
                if grid[i][ii]:  # print if exist value otherwise would cause error.
                    text = self.font.render(f'{grid[i][ii]}', False, 'White')
                    text_rect = text.get_rect(center=coordinate)
                    screen.blit(text, text_rect)

    def set_target_column(self):  # TODO MOVE TO CONTROLS, I DONT KNOW HOW BUT THIS MUST BE IN OTHER CLASS
        right_click = pg.mouse.get_pressed()[0]  # index 0 is the right mouse button
        mouse_pos = pg.mouse.get_pos()
        for i, rect in enumerate(self.grid_rects.values(), start=1):
            if rect.collidepoint(mouse_pos) and right_click and self.player.dice.number and not self.target_column:
                # Select the dice position column
                match i:
                    case 1:
                        self.target_column = 1
                        print(f'The dice position {self.target_column}', self.player.player.name)
                    case 2:
                        self.target_column = 2
                        print(f'The dice position {self.target_column}', self.player.player.name)
                    case 3:
                        self.target_column = 3
                        print(f'The dice position {self.target_column}', self.player.player.name)

    def add_to_column(self):
        """Add the dice to the selected column"""
        if self.player.is_turn and self.target_column:
            self.player.add(self.target_column, self.player.dice.number)
            print('grid', self.player.grid, self.player.player.name)

    def update_points(self):
        """Change players turn, update values and reset to avoid errors."""
        if self.player.is_turn and self.target_column:
            self.player.points_board.update_column_points(self.player.grid, self.target_column)
            self.player.points_board.update_total_score()
            print('Points', self.player.points_board.points, self.player.player.name)

    def update_opponent_game(self, opponent):
        """Update the game of the opponent player."""
        if self.player.is_turn and self.target_column and self.player.dice.number:
            GameModel.remove_and_update_opponent_board(opponent, self.target_column, self.player.dice.number)

    def update_turn(self, func_update_total_score, opponent):
        if self.player.is_turn and self.target_column:
            self.player.dice.number = None
            self.target_column = None
            self.player.is_turn = False
            opponent.is_turn = True
            print('current_player', self.player.player.name)
            print('opponent', opponent.player.name)
            # This make a call back to update the Turns in the game.
            func_update_total_score()

    def update(self, screen, p1_grid: dict, p2_grid: dict, p1_grid_point: dict, p2_grid_point: dict,
               removed_dices_player: dict, opponent, func_update_total_score) -> None:

        self.assign_grid_to_board_color(p1_grid, p2_grid)
        self.assign_points_to_board_color(p1_grid_point, p2_grid_point)
        self.assign_removed_events(removed_dices_player)
        self.show_slash(screen, 600, 200)
        self.set_grid_rects(screen)
        self.set_grid_numbers(screen, self.grid_main)
        self.set_grid_points(screen, self.grid_points)
        self.proces_removed_events()
        # Selection of dice position
        self.set_target_column()
        self.add_to_column()
        self.update_points()
        self.update_opponent_game(opponent)
        self.update_turn(func_update_total_score, opponent)
