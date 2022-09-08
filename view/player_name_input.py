# Import
import pygame as pg
from config import config
from view.menu import ButtonView


class PlayerNameTextInput:

    def __init__(self, player1, player2):
        self.screen = pg.display.get_surface()
        # Text
        self.p1 = player1
        self.p2 = player2
        self.text_input = pg.sprite.Group()
        self.text_input.add(TextInput(600, 300, self.p1, 'Red'))
        self.text_input.add(TextInput(600, 600, self.p2, 'Green'))
        # Menu
        self.menu = pg.sprite.Group(ButtonView(600, 920, 'Go to match', btn_name='match'))

    def show_titles(self):
        # Title

        title_font = pg.font.Font(config.get('FONT').get('MAGIC'), 100)
        title = title_font.render('Select players Names', False, 'Black')
        title_rect = title.get_rect(center=(600, 100))
        # Subtitles
        sub_title_font = pg.font.Font(config.get('FONT').get('MAGIC'), 30)
        player1 = sub_title_font.render('Player1 Name', False, 'Black')
        player1_rect = player1.get_rect(center=(600, 230))
        player2 = sub_title_font.render('Player2 Name', False, 'Black')
        player2_rect = player2.get_rect(center=(600, 530))
        # Show text
        self.screen.blit(title, title_rect)
        self.screen.blit(player1, player1_rect)
        self.screen.blit(player2, player2_rect)

    def show_help_text_btn(self):
        """Display a Text in the button to notify that the player need to add text to the display"""
        if not self.p1.player.name or not self.p2.player.name:
            font = pg.font.Font(config.get('FONT').get('MAGIC'), 30)
            help_btn_text = font.render('Add Players Names', False, 'White')
            help_btn_text_rect = help_btn_text.get_rect(center=(600, 920))
            self.screen.blit(help_btn_text, help_btn_text_rect)

    def run(self, game_state):
        # Titles
        self.show_titles()
        # Text
        self.text_input.draw(self.screen)
        self.text_input.update()
        # Button
        self.menu.draw(self.screen)
        self.show_help_text_btn()
        if self.p1.player.name and self.p2.player.name:
            self.menu.update(game_state)


class TextInput(pg.sprite.Sprite):
    SIZE = (400, 160)

    def __init__(self, x_pos: int, y_pos: int, player, color: str):
        super(TextInput, self).__init__()
        self.color: str = color
        self.player = player
        self.x: int = x_pos
        self.y: int = y_pos
        self.screen = pg.display.get_surface()
        self.image = pg.transform.scale(pg.image.load(config.get('IMG')  # Select the board color
                                                      .get('GREEN_BTN' if self.color == 'Green' else 'RED_BTN'))
                                        .convert_alpha(), self.SIZE)

        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.font = pg.font.Font(config.get('FONT').get('MAGIC'), 30)
        self.is_click: bool = False
        self.is_key_press: bool = False
        self.is_box_selected: bool = False
        self.text_area: str = ''

    def proces_mouse_select_box(self):
        # Click
        mouse = pg.mouse.get_pressed()
        if self.rect.collidepoint(pg.mouse.get_pos()) and not self.is_box_selected:
            if mouse[0] and not self.is_click:
                self.is_click = True
                self.is_box_selected = True

        if not self.rect.collidepoint(pg.mouse.get_pos()) and self.is_box_selected:
            if mouse[0] and not self.is_click:
                self.is_click = True
                self.is_box_selected = False

        if not mouse[0] and self.is_click:
            self.is_click = False

    def proces_text_inputs(self):
        """Proces the text inputs in the keyboard"""
        keys = pg.key.get_pressed()
        if self.is_box_selected and len(self.text_area) < 20:  # This help to avoid big names inputs
            if keys[pg.K_BACKSPACE] and not self.is_key_press:
                self.is_key_press = True
                self.text_area = self.text_area[:-1]
            elif keys[pg.K_a] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'a'
            elif keys[pg.K_b] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'b'
            elif keys[pg.K_c] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'c'
            elif keys[pg.K_d] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'd'
            elif keys[pg.K_e] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'e'
            elif keys[pg.K_f] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'f'
            elif keys[pg.K_g] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'g'
            elif keys[pg.K_h] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'h'
            elif keys[pg.K_i] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'i'
            elif keys[pg.K_j] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'j'
            elif keys[pg.K_k] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'k'
            elif keys[pg.K_l] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'l'
            elif keys[pg.K_m] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'm'
            elif keys[pg.K_n] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'n'
            elif keys[pg.K_o] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'o'
            elif keys[pg.K_p] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'p'
            elif keys[pg.K_q] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'q'
            elif keys[pg.K_r] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'r'
            elif keys[pg.K_s] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 's'
            elif keys[pg.K_t] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 't'
            elif keys[pg.K_u] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'u'
            elif keys[pg.K_v] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'v'
            elif keys[pg.K_d] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'd'
            elif keys[pg.K_x] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'x'
            elif keys[pg.K_y] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'y'
            elif keys[pg.K_z] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += 'z'
            elif keys[pg.K_1] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '1'
            elif keys[pg.K_2] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '2'
            elif keys[pg.K_3] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '3'
            elif keys[pg.K_4] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '4'
            elif keys[pg.K_5] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '5'
            elif keys[pg.K_6] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '6'
            elif keys[pg.K_7] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '7'
            elif keys[pg.K_8] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '8'
            elif keys[pg.K_9] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '9'
            elif keys[pg.K_0] and not self.is_key_press:
                self.is_key_press = True
                self.text_area += '0'

        # This if statement is an elegant way to identify if any of the key is pressed
        # Because pygame return an array of Boolean results. If any of the keys is pressed it will return 1
        # If any key is pressed it will return 0
        if not sum(tuple(keys)) and self.is_key_press:
            self.is_key_press = False

    def show_box_activate(self):
        """Paint the input are with white if write is activate, else paint grey the input area if write
        is not activate"""
        surface = pg.Surface((300, 50))
        rect = surface.get_rect(center=(self.x, self.y))
        if not self.is_box_selected:
            pg.draw.rect(self.screen, 'Grey', rect, border_radius=20)
            if not self.text_area:  # Display a help text if it doesn't is any character in the input display
                help_input = self.font.render('Enter your name', False, 'White')
                help_input_rect = help_input.get_rect(center=(self.x, self.y))
                self.screen.blit(help_input, help_input_rect)
        else:
            pg.draw.rect(self.screen, 'White', rect, border_radius=20)

    def show_text_input(self):
        text_input_player = self.font.render(self.text_area.title(), False, 'Black')
        text_input_player_rect = text_input_player.get_rect(center=(self.x, self.y))
        self.screen.blit(text_input_player, text_input_player_rect)

    def update_player_name(self):
        self.player.player.name = self.text_area.title()

    def update(self):
        self.show_box_activate()
        self.proces_mouse_select_box()
        self.proces_text_inputs()
        self.show_text_input()
        self.update_player_name()
