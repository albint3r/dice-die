# Import
import pygame as pg
import random


class MenuView:
    TIMER_DELAY = 500  # 0.5 seconds
    FONT_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\font\BebasNeue-Regular.ttf'

    def __init__(self):
        self.screen = pg.display.get_surface()
        # Timer Dice Falling
        self.timer_event = pg.USEREVENT + 2
        pg.time.set_timer(self.timer_event, self.TIMER_DELAY)
        # Logo
        self.logo = pg.sprite.GroupSingle(LogoGame(600, 100))
        self.dices_group = pg.sprite.Group()
        # Buttons
        self.buttons_group = pg.sprite.Group()
        self.start_btn = ButtonView(600, 300, 'Start new game')
        self.how_to_play_btn = ButtonView(600, 500, 'How to Play?')
        self.leader_board_btn = ButtonView(600, 700, 'Leader Board')
        # Add button to group
        self.set_buttons_to_group()
        # Add Text
        self.font_brand = pg.font.Font(self.FONT_ROOT, 20)
        self.albinter_text = self.font_brand.render('Albinter Inc', False, 'Black')
        self.version_text = self.font_brand.render('Version 1.0.0', False, 'Black')

    def show_brand_text(self):
        self.screen.blit(self.albinter_text, (20, 950))
        self.screen.blit(self.version_text, (20, 970))

    def create_new_dice(self, event):
        """Create dices that are falling"""
        if event.type == self.timer_event:
            self.dices_group.add(FallingDicesView())

    def set_buttons_to_group(self):
        self.buttons_group.add(self.start_btn)
        self.buttons_group.add(self.how_to_play_btn)
        self.buttons_group.add(self.leader_board_btn)

    def run(self, game_state):
        # Logo
        self.logo.draw(self.screen)
        # Brand text
        self.show_brand_text()
        # Falling Dices
        self.dices_group.draw(self.screen)
        self.dices_group.update()
        # Buttons
        self.buttons_group.draw(self.screen)
        self.buttons_group.update(game_state)


class FallingDicesView(pg.sprite.Sprite):
    RAND_INT = [(50, 50), (50, 50), (50, 50), (150, 150), (200, 200)]
    DICE_IMG = {1: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\1.png',
                2: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\2.png',
                3: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\3.png',
                4: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\4.png',
                5: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\5.png',
                6: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\dice\6.png',
                7: r'C:\Users\albin\PycharmProjects\dice_&_die\statics\bitcoin.png'}

    def __init__(self):
        super().__init__()
        self.scree = pg.display.get_surface()
        self.random_index = random.randint(1, 7)
        self.speed = 1
        self.size = random.choice(self.RAND_INT)
        self.image = pg.transform.scale(pg.image.load(self.DICE_IMG.get(self.random_index)).convert_alpha(), self.size)
        self.rect = self.image.get_rect(center=(random.randint(0, 1200), -100))

    def hold_with_mouse(self):
        mouse_pos = pg.mouse.get_pos()
        mose = pg.mouse.get_pressed()
        if self.rect.collidepoint(mouse_pos) and mose[0]:
            self.rect.y -= 150
            self.speed = -15

    def update_position(self):
        self.rect.y += self.speed
        self.speed += 1

    def destroy_unseen(self):
        if self.rect.top == 1050:
            self.kill()

    def update(self):
        self.destroy_unseen()
        self.update_position()
        self.hold_with_mouse()


class ButtonView(pg.sprite.Sprite):
    SIZE = (400, 200)
    FONT_ROOT = r'C:\Users\albin\PycharmProjects\dice_&_die\statics\font\Magical Story.ttf'

    def __init__(self, x: float, y: float, text: str):
        super().__init__()
        self.button_type = (r'C:\Users\albin\PycharmProjects\dice_&_die\statics\gree_button.png',
                            r'C:\Users\albin\PycharmProjects\dice_&_die\statics\red_button.png')

        self.screen = pg.display.get_surface()
        self.img_index = 1
        self.btn_name = text.lower()
        self.image = pg.transform.scale(pg.image.load(self.button_type[self.img_index]).convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=(x, y))
        # Font text
        self.font = pg.font.Font(self.FONT_ROOT, 50)
        self.text = self.font.render(text.title(), False, 'White')
        self.text_rect = self.text.get_rect(center=(x, y))
        # Sound
        self.sound = pg.mixer.Sound(r'C:\Users\albin\PycharmProjects\dice_&_die\statics\sound\piano_key.WAV')
        self.is_sound = False
        self.is_click = False

    def set_button_color(self):
        self.image = pg.transform.scale(pg.image.load(self.button_type[self.img_index]).convert_alpha(), self.SIZE)

    def show_text(self):
        self.screen.blit(self.text, self.text_rect)

    def press_button(self, game_state, GameController=None):
        mouse = pg.mouse.get_pressed()

        if self.rect.collidepoint(pg.mouse.get_pos()):
            # Change the index to have green o red color if hover on the button
            self.img_index = 0
            # This helps in the hover effect
            if self.is_sound:
                self.sound.play()
                self.is_sound = False

            if mouse[0] and not self.is_click:  # If right click do any of the actions below
                self.is_click = True
                match self.btn_name:
                    case 'start new game':
                        game_state['menu'] = False
                        game_state['match'] = True  # <----------
                        game_state['how_to_play'] = False
                        game_state['leader_board'] = False
                        game_state['winner'] = False
                        game_state['retry'] = False

                    case 'how to play?':
                        print('click how to')

                    case 'leader board':
                        print('click leader board')

                    case 'back to menu':
                        game_state['menu'] = True  # <----------
                        game_state['match'] = False
                        game_state['how_to_play'] = False
                        game_state['leader_board'] = False
                        game_state['winner'] = False
                        game_state['retry'] = False

                    case 'retry':
                        game_state['menu'] = False
                        game_state['match'] = False
                        game_state['how_to_play'] = False
                        game_state['leader_board'] = False
                        game_state['winner'] = False
                        game_state['retry'] = True  # <----------

            # This helps to only register one click
            elif not mouse[0] and self.is_click:
                self.is_click = False

        else:
            self.img_index = 1
            self.sound.stop()
            self.is_sound = True

    def update(self, game_state):
        self.press_button(game_state)
        self.show_text()
        self.set_button_color()


class LogoGame(pg.sprite.Sprite):
    SIZE = (600, 600)
    IMG_ROOT = r"C:\Users\albin\PycharmProjects\dice_&_die\statics\logo.png"

    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(self.IMG_ROOT).convert_alpha(), self.SIZE)
        self.rect = self.image.get_rect(center=(x, y))
