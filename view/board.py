# Import
import pygame as pg
import random
# Model
from model.game_engine import GameModel


class BoarGameView(pg.sprite.Sprite):
    RED_BOARD_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\red_board.png'
    GREEN_BOARD_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\green_board.png'
    RED_SLASH_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\slash1.png'
    BLUE_SLASH_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\slash2.png'
    SLASH_SOUND = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\sound\slash1_sound.mp3'
    # Damage
    BROKEN1_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\broken1.png'
    BROKEN2_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\broken2.png'
    BROKEN3_IMG = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\broken3.png'
    # Arrow
    RED_ARROW_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\red_arrow.png'
    GREEN_ARROW_IMG_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\green_arrow.png'
    # FONT_ROOT = r'../statics/font/Magical Story.ttf'
    FONT_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\font\Magical Story.ttf'
    BOARDS_SIZE = (600, 400)
    COL_SIZE = (163, 247)

    def __init__(self, board_color: str, player_board):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.color = board_color
        self.player = player_board
        self.font = pg.font.Font(self.FONT_ROOT, 60)
        self.font_points = pg.font.Font(self.FONT_ROOT, 40)
        # Action Font
        self.font_action_indicator = pg.font.Font(self.FONT_ROOT, 30)
        self.action_text = self.font_action_indicator.render('Press Space', False, 'Black')
        # Player Name
        self.font_name = pg.font.Font(self.FONT_ROOT, 45)
        # Target Column to put the dice result
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

        self.dic_coor = {1: self.col1_coor, 2: self.col2_coor, 3: self.col3_coor}

        # Grid Invisible Blocks
        self.grid_rects: dict = dict()
        self.grid_main: dict | None = None
        self.grid_points: dict | None = None
        self.col_image = pg.Surface(self.COL_SIZE)
        self.removed_events: dict | None = None  # is a list that contain boolean indicators to remove dices
        # This is the col targe
        self.removed_events_location_coordinates_all: tuple | None = None
        self.coordinates_to_slash: list[tuple] = list()
        self.cooldown_slash: int = 3
        self.slash_sound_action: bool = True
        # Board Damage
        self.damages_img_lst: list = list()
        self.damages_rects_lst: list = list()

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

    def assign_removed_events(self, removed_dices_player: dict) -> None:
        """Assign the removed dice evento to each board depends on the color
        This helps to identify where would be printed a X mark when a dice is destroyed
        """

        # {1: None}
        # {1: [True, False, False]}
        for player, removed_events in removed_dices_player.items():
            if self.color == 'Red' and player == 1:
                self.removed_events = removed_events

            if self.color == 'Green' and player == 2:
                self.removed_events = removed_events

    def get_remove_coordinates(self, targe_column: int):
        """Return the list of tuples with the coordinates of the B"""
        return self.dic_coor.get(targe_column)

    def proces_removed_events(self):
        """This method would activate the removed dice animation effect on the player board."""

        # Validate if exist events and if the event is Not None
        # The events must be a list -> [True, True, False]  or None
        if self.removed_events and list(self.removed_events.values())[0]:

            # This is an integer to extract the column tuple
            column_event_index = list(self.removed_events.keys())[0]
            removed_events_bool_list = list(self.removed_events.values())[0]
            # Assign the only one column with the True false target location.
            self.removed_events_location_coordinates_all = self.dic_coor.get(column_event_index)

            # Create a single list of tuples, with the specific location target.
            # Example:
            # ******************************************************************************
            # [True, True, False]  -> Because there is 2 true
            # [(430, 635), (770, 635)]  -> The result list only have 2 values inside
            # ******************************************************************************
            # Execute an if else statement to identify only the index with the true values
            # This helps to select only the tuple COORDINATES in the same location.
            # This would be iterated to display the X slash in the coordinates target
            if removed_events_bool_list[0]:
                self.coordinates_to_slash.append(self.removed_events_location_coordinates_all[0])
            if removed_events_bool_list[1]:
                self.coordinates_to_slash.append(self.removed_events_location_coordinates_all[1])
            if removed_events_bool_list[2]:
                self.coordinates_to_slash.append(self.removed_events_location_coordinates_all[2])

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

    def show_grid_numbers(self, screen, grid: dict[list, list, list]) -> None:
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
        col_coordinates_list = self.get_grid_coordinates()
        self.validate_and_show_grid_numbers(screen, col_coordinates_list, grid)

    def get_grid_coordinates(self) -> tuple:
        return self.col1_coor, self.col2_coor, self.col3_coor

    def show_grid_points(self, screen, grid_point: dict):
        """Validate the Board Color Player and Display it the Points Score of each player."""
        if self.color == 'Red':
            col_coordinates_lst = (430, 135), (600, 135), (770, 135)

        if self.color == 'Green':
            col_coordinates_lst = (430, 870), (600, 870), (770, 870)

        for i, col in enumerate(col_coordinates_lst, start=1):
            text = self.font_points.render(f'{grid_point[i]}', False, 'Black')
            text_rect = text.get_rect(center=col)
            screen.blit(text, text_rect)

    def show_slash(self):
        """Display slash animation
        Only run if it had a coordinate in the list. After run N times (cooldown slash) it will
        pop the coordinate and this will return False. But if it had another coordinate it will display it to.
        """
        if self.coordinates_to_slash and self.cooldown_slash:
            # Show the slash image 3 frame
            # Active the slash sound one time
            # After activate the sound it deactivate
            if self.slash_sound_action:
                slash_sound = pg.mixer.Sound(self.SLASH_SOUND)
                slash_sound.play()
                self.slash_sound_action = False
                self.add_broken()
            # Create Slash image
            slash_img = pg.transform.scale(pg.image.load(self.RED_SLASH_IMG).convert_alpha(), (500, 500))
            # Select the tuple and add 30px to x to center the slash with the number
            coordinates = self.coordinates_to_slash[0]
            slash_img_rect = slash_img.get_rect(center=(coordinates[0] + 35, coordinates[1]))
            self.screen.blit(slash_img, slash_img_rect)
            # Set the time duration of the slash image
            self.cooldown_slash -= 1
            # If the time duration is 0 it will remove the coordinates of the slash target
            # Reset the cooldown duration and activate again the sound for the next animation.
            if not self.cooldown_slash:
                self.coordinates_to_slash.pop(0)
                self.cooldown_slash = 3
                self.slash_sound_action = True

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

    def add_broken(self):
        """Create a broken objet to display in front of the board to create the ilution of damage"""
        if self.color == 'Red':
            x_range = random.randint(350, 820)
            y_range = random.randint(150, 370)

        if self.color == 'Green':
            x_range = random.randint(350, 820)
            y_range = random.randint(600, 800)

        # Select a random Broken image to display. This have a 66% of be a small broke, an 33% of a big broken
        random_img = random.choice([self.BROKEN2_IMG, self.BROKEN2_IMG, self.BROKEN1_IMG])

        angle_rotation = random.randint(0, 360)  # Rotate randomly the image to create the sensation o variety
        image = pg.transform.rotate(pg.transform.scale(pg.image.load(random_img).convert_alpha(), (40, 40)),
                                    angle_rotation)
        image_rect = self.image.get_rect(topleft=(x_range, y_range))
        self.damages_img_lst.append(image)
        self.damages_rects_lst.append(image_rect)

    def show_damage(self):
        """Display the damage image in front of the board player"""
        if self.damages_img_lst and self.damages_rects_lst:
            for image, damage in zip(self.damages_img_lst, self.damages_rects_lst):
                self.screen.blit(image, damage)

    def show_player_name(self):

        if self.color == 'Red':
            name_text = self.font_name.render(f'{self.player.player.name}', False, 'Black')
            name_rect = name_text.get_rect(center=(200, 120))
            self.screen.blit(name_text, name_rect)

        if self.color == 'Green':
            name_text = self.font_name.render(f'{self.player.player.name}', False, 'Black')
            name_rect = name_text.get_rect(center=(1000, 890))
            self.screen.blit(name_text, name_rect)


    def show_turn_indicator(self):
        """Display if it is the player turn an arrow and a text to indicate the player turn."""

        if self.player.dice.number:
            self.action_text = self.font_action_indicator.render('Select Column', False, 'Black')
        else:
            self.action_text = self.font_action_indicator.render('Press Space', False, 'Black')

        if self.color == 'Red' and self.player.is_turn:
            text_rect = self.action_text.get_rect(center=(200, 400))
            arrow_img = pg.transform.scale(pg.image.load(self.RED_ARROW_IMG_ROOT).convert_alpha(), (100, 70))
            arrow_rect = arrow_img.get_rect(center=(200, 350))
            self.screen.blit(self.action_text, text_rect)
            self.screen.blit(arrow_img, arrow_rect)


        if self.color == 'Green' and self.player.is_turn:
            text_rect = self.action_text.get_rect(center=(1000, 605))
            arrow_img = pg.transform.scale(pg.image.load(self.GREEN_ARROW_IMG_ROOT).convert_alpha(), (100, 70))
            arrow_rect = arrow_img.get_rect(center=(1000, 650))
            self.screen.blit(self.action_text, text_rect)
            self.screen.blit(arrow_img, arrow_rect)

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

    def update(self, p1_grid_copy: dict, p2_grid_copy: dict, p1_grid_point: dict, p2_grid_point: dict,
               removed_dices_player: dict, opponent, func_update_total_score) -> None:

        self.assign_grid_to_board_color(p1_grid_copy, p2_grid_copy)
        self.assign_points_to_board_color(p1_grid_point, p2_grid_point)
        self.assign_removed_events(removed_dices_player)
        # Design
        self.set_grid_rects(self.screen)
        self.show_damage()
        self.show_grid_numbers(self.screen, self.grid_main)
        self.show_grid_points(self.screen, self.grid_points)
        self.show_turn_indicator()
        self.show_slash()
        self.show_player_name()
        # Slash events
        self.proces_removed_events()
        # Selection of dice position
        self.set_target_column()
        self.add_to_column()
        self.update_points()
        self.update_opponent_game(opponent)
        self.update_turn(func_update_total_score, opponent)
