# Import
import pygame as pg
from config import config
from view.menu import ButtonView


class HowToPlayView:

    def __init__(self):
        self.screen = pg.display.get_surface()
        self.points_system = pg.sprite.GroupSingle(PointsSystem())
        self.destroy_system = pg.sprite.GroupSingle(DestroySystem())
        self.menu = pg.sprite.Group()
        self.menu.add(ButtonView(600, 920, 'Back to menu'))

    def run(self, game_state):
        # Points Sys
        self.points_system.draw(self.screen)
        self.points_system.update()
        # Destroy Sys
        self.destroy_system.draw(self.screen)
        self.destroy_system.update()
        # Menu
        self.menu.draw(self.screen)
        self.menu.update(game_state)


class PointsSystem(pg.sprite.Sprite):

    def __init__(self):
        super(PointsSystem, self).__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.image.load(config.get('IMG').get('POINTS_SYSTEM')).convert_alpha()
        self.rect = self.image.get_rect(center=(600, 300))
        self.font_title = pg.font.Font(config.get('FONT').get('MAGIC'), 35)
        self.font_body = pg.font.Font(config.get('FONT').get('BEBAS'), 16)

    def show_title(self):
        """Show the title of the point system section"""
        title = self.font_title.render('How to get points?', False, 'Black')
        title_rect = title.get_rect(center=(600, 50))
        self.screen.blit(title, title_rect)

    def show_body_text(self):
        """Show the title of the point system section"""
        paragraph = [
            'Each Turn you roll the dice and put the result in one of the three columns on your board. If you have only one type of number in that column,',
            'the value of the number will be multiply by 1, but if you add more numbers of the same value, you multiply x2 or x3. ']

        start_pos = 60
        height = 50

        for text in paragraph:
            body_text = self.font_body.render(text, False, 'Black')
            body_text_rect = body_text.get_rect(center=(600, start_pos + height))
            self.screen.blit(body_text, body_text_rect)
            start_pos = start_pos + height

    def update(self):
        self.show_title()
        self.show_body_text()


class DestroySystem(pg.sprite.Sprite):

    def __init__(self):
        super(DestroySystem, self).__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.image.load(config.get('IMG').get('DESTROY_SYSTEM')).convert_alpha()
        self.rect = self.image.get_rect(center=(600, 700))
        self.font_title = pg.font.Font(config.get('FONT').get('MAGIC'), 35)
        self.font_body = pg.font.Font(config.get('FONT').get('BEBAS'), 16)

    def show_title(self):
        """Show the title of the point system section"""
        title = self.font_title.render('2) How to destroy opponent numbers?', False, 'Black')
        title_rect = title.get_rect(center=(600, 450))
        self.screen.blit(title, title_rect)

    def show_body_text(self):
        """Show the title of the point system section"""
        paragraph = [
            'When you roll the dice, you select a target column, if the other player have the same value inside the same column, it will destroy it all the numbers',
            'with the same value.']

        start_pos = 460
        height = 50

        for text in paragraph:
            body_text = self.font_body.render(text, False, 'Black')
            body_text_rect = body_text.get_rect(center=(600, start_pos + height))
            self.screen.blit(body_text, body_text_rect)
            start_pos = start_pos + height

    def update(self):
        self.show_title()
        self.show_body_text()
