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
        if board_color == 'Red':
            self.x, self.y = (600, 250)
            self.image = pg.transform.scale(pg.image.load(self.RED_BOARD_IMG_ROOT).convert_alpha(), self.BOARDS_SIZE)
            self.rect = self.image.get_rect(center=(self.x, self.y))
        if board_color == 'Green':
            self.x, self.y = (600, 750)
            self.image = pg.transform.scale(pg.image.load(self.GREEN_BOARD_IMG_ROOT).convert_alpha(), self.BOARDS_SIZE)
            self.rect = self.image.get_rect(center=(self.x, self.y))

        # Grid Invisible Blocks
        self.grid: dict = dict()
        self.col_image = pg.Surface(self.COL_SIZE)

    def set_grid_rects(self, screen, show: bool = False):
        """Set grid Rectangles By there type of color.
        This helps to detect better the click collision to select the dice position.
        """
        if self.color == 'Red':
            coordinates = ((354, 154), (520, 154), (682, 154))
            self.grid = {i: self.col_image.get_rect(topleft=coordinate) for i, coordinate in enumerate(coordinates)}

        if self.color == 'Green':
            coordinates = ((354, 592), (520, 592), (682, 592))
            self.grid = {i: self.col_image.get_rect(topleft=coordinate) for i, coordinate in enumerate(coordinates)}

        if show:
            for key, val in self.grid.items():
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
            self.set_grid_numbers_validated(screen, col_coordinates_list, grid)

        if self.color == 'Green':
            col1_coor = ((430, 635), (430, 725), (430, 810))
            col2_coor = ((600, 635), (600, 725), (600, 810))
            col3_coor = ((770, 635), (770, 725), (770, 810))
            col_coordinates_list = (col1_coor, col2_coor, col3_coor)
            self.set_grid_numbers_validated(screen, col_coordinates_list, grid)

    def set_grid_numbers_validated(self, screen, col_coordinates_list: tuple, grid: dict[list, list, list]):
        for i, col_cor in enumerate(col_coordinates_list, start=1):
            for ii, coordinate in enumerate(col_cor):
                if grid[i][ii]:
                    text = self.font.render(f'{grid[i][ii]}', False, 'White')
                    text_rect = text.get_rect(center=coordinate)
                    screen.blit(text, text_rect)

    def mouse_coll(self):
        right_click = pg.mouse.get_pressed()[0]  # index 0 is the right mouse button
        mouse_pos = pg.mouse.get_pos()
        for i, rect in enumerate(self.grid.values(), start=1):
            if rect.collidepoint(mouse_pos) and right_click:
                print(f'Click col {i} {self.color}')

    def update(self, screen, grid) -> None:
        self.set_grid_rects(screen)
        self.set_grid_numbers(screen, grid)
        self.mouse_coll()
