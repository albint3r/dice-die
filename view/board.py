# Import
import pygame as pg


class BoarGameView(pg.sprite.Sprite):
    RED_BOARD_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\red_board.png'
    GREEN_BOARD_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\green_board.png'
    FONT_ROOT = r'../statics/font/Magical Story.ttf'
    BOARDS_SIZE = (600, 400)
    COL_SIZE = (163, 247)

    def __init__(self, board_color: str):
        super().__init__()
        self.color = board_color
        self.font = pg.font.Font(self.FONT_ROOT, 60)
        self.font_points = pg.font.Font(self.FONT_ROOT, 40)

        if board_color == 'Red':
            self.x, self.y = (600, 250)
            self.image = pg.transform.scale(pg.image.load(self.RED_BOARD_IMG_ROOT).convert_alpha(), self.BOARDS_SIZE)
            self.rect = self.image.get_rect(center=(self.x, self.y))
        if board_color == 'Green':
            self.x, self.y = (600, 750)
            self.image = pg.transform.scale(pg.image.load(self.GREEN_BOARD_IMG_ROOT).convert_alpha(), self.BOARDS_SIZE)
            self.rect = self.image.get_rect(center=(self.x, self.y))

        # Grid Invisible Blocks
        self.grid_rects: dict = dict()
        self.grid_original: dict | None = None
        self.grid_points: dict | None = None
        self.col_image = pg.Surface(self.COL_SIZE)

    def assign_grid_to_board_color(self, grid_p1, grid_p2):
        """Assign the Grid Board of the player depends on the color"""
        if self.color == 'Red':
            self.grid_original = grid_p1
        if self.color == 'Green':
            self.grid_original = grid_p2

    def assign_points_to_board_color(self, points_p1, points_p2):
        """Assign the Grid Board of the player depends on the color"""
        if self.color == 'Red':
            self.grid_points = points_p1
        if self.color == 'Green':
            self.grid_points = points_p2

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
            col1_coor = ((430, 200), (430, 285), (430, 375))
            col2_coor = ((600, 200), (600, 285), (600, 375))
            col3_coor = ((770, 200), (770, 285), (770, 375))
            col_coordinates_list = (col1_coor, col2_coor, col3_coor)
            self.validate_and_show_grid_numbers(screen, col_coordinates_list, grid)

        if self.color == 'Green':
            col1_coor = ((430, 635), (430, 725), (430, 810))
            col2_coor = ((600, 635), (600, 725), (600, 810))
            col3_coor = ((770, 635), (770, 725), (770, 810))
            col_coordinates_list = (col1_coor, col2_coor, col3_coor)
            self.validate_and_show_grid_numbers(screen, col_coordinates_list, grid)

    def set_grid_points(self, screen, grid_point: dict):

        if self.color == 'Red':
            col_coordinates_lst = (430, 135), (600, 135), (770, 135)

        if self.color == 'Green':
            col_coordinates_lst = (430, 870), (600, 870), (770, 870)

        for i, col in enumerate(col_coordinates_lst, start=1):
            text = self.font_points.render(f'{grid_point[i]}', False, 'Black')
            text_rect = text.get_rect(center=col)
            screen.blit(text, text_rect)

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

    def mouse_coll(self):
        right_click = pg.mouse.get_pressed()[0]  # index 0 is the right mouse button
        mouse_pos = pg.mouse.get_pos()
        for i, rect in enumerate(self.grid_rects.values(), start=1):
            if rect.collidepoint(mouse_pos) and right_click:
                print(f'Click col {i} {self.color}')

    def update(self, screen, p1_grid: dict, p2_grid: dict, p1_grid_point: dict, p2_grid_point: dict) -> None:
        self.assign_grid_to_board_color(p1_grid, p2_grid)
        self.assign_points_to_board_color(p1_grid_point, p2_grid_point)
        self.set_grid_rects(screen)
        self.set_grid_numbers(screen, self.grid_original)
        self.set_grid_points(screen, self.grid_points)
        self.mouse_coll()
