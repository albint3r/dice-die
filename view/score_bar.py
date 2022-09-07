# Import
import pygame as pg
import datetime as dt
from config import config


class ScoreBarView(pg.sprite.Sprite):
    WIDTH, HEIGHT = (400, 25)  # Bar Size
    X_POS, Y_POS = (600, 500)  # middle of the screen
    COLOR_RED = '#F22B56'
    COLOR_GREEN = '#78BD91'
    COLOR_RED_SHADOW = '#BB314F'
    COLOR_GREEN_SHADOW = '#4D8F81'
    BAR_SPEED = 5
    BORDER_RADIUS = 5

    def __init__(self):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.original_image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.original_image.fill(self.COLOR_GREEN)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.X_POS, self.Y_POS))
        self.red_bar_size = 200
        self.font = pg.font.Font(config.get('FONT').get('BEBAS'), 22)  # Todo ADD FONT TEXT
        # Halo
        self.points_font = pg.font.Font(config.get('FONT').get('MAGIC'), 100)
        # Red
        self.red_halo_img = pg.transform.scale(pg.image.load(config.get('IMG').get('RED_HALO')).convert_alpha(), (200, 200))
        self.red_halo_rect = self.red_halo_img.get_rect(center=(200, 500))
        # Green
        self.green_halo_img = pg.transform.scale(pg.image.load(config.get('IMG').get('GREEN_HALO')).convert_alpha(), (200, 200))
        self.green_halo_rect = self.green_halo_img.get_rect(center=(1000, 500))

    def set_rounded(self):
        """Make round corners in the score bar"""
        round_rect_image = pg.Surface(self.original_image.get_size(), pg.SRCALPHA)
        # The 0,0 is to align the new border images with the old bar rect.
        pg.draw.rect(round_rect_image, (255, 255, 255), (0, 0, *self.original_image.get_size()),
                     border_radius=self.BORDER_RADIUS)
        self.image = self.original_image.copy().convert_alpha()
        self.image.blit(round_rect_image, (0, 0), None, pg.BLEND_RGBA_MIN)

    def set_shadows(self):
        x_less = 3
        y_less = 3
        shadow_image = pg.Surface(self.original_image.get_size())
        shadow_rect = shadow_image.get_rect(center=(self.X_POS - x_less, self.Y_POS + y_less))
        pg.draw.rect(self.screen, self.COLOR_GREEN_SHADOW, shadow_rect, border_radius=self.BORDER_RADIUS)

    def show_red_bar(self):
        """Create the Red Bar Score"""
        # This is a threshold to display the red bar ok.
        # Below this value it would create a rectangle square in the left
        red_bar_image = pg.Surface((self.red_bar_size, 25))
        red_bar_rect = red_bar_image.get_rect(midleft=(self.rect.x, self.Y_POS))
        pg.draw.rect(self.screen, self.COLOR_RED, red_bar_rect, border_radius=self.BORDER_RADIUS)

    def calculate_bar_per(self, p1_score: int, p2_score: int) -> int:
        """Update the Bar Score Image Size to create the sensation of motion"""
        total_points = p1_score + p2_score
        # Red Bar Player
        if total_points:
            p1_points_per = p1_score / total_points
            return int(self.WIDTH * p1_points_per)
        else:
            return 200

    def update_bar_size(self, p1_score: int, p2_score: int):
        """Update the size frame by frame of the Red Bar Size"""
        new_red_bar_size = self.calculate_bar_per(p1_score, p2_score)

        if self.red_bar_size > new_red_bar_size and self.red_bar_size > new_red_bar_size + self.BAR_SPEED:
            self.red_bar_size -= self.BAR_SPEED
        elif self.red_bar_size < new_red_bar_size and self.red_bar_size < new_red_bar_size - self.BAR_SPEED:
            self.red_bar_size += self.BAR_SPEED
        else:
            self.red_bar_size = new_red_bar_size

    def show_turns_text(self, turn):
        text = self.font.render(f'Turn: {turn}', False, 'Black')
        text_rect = text.get_rect(center=(self.X_POS, self.Y_POS - 30))
        self.screen.blit(text, text_rect)

    def show_red_total_points(self, p1_total_point):
        """Display the total red points"""
        # Points
        font_img = self.points_font.render(f"{p1_total_point}", False, 'Black')
        font_rect = font_img.get_rect(center=(200, 510))
        # Show
        self.screen.blit(font_img, font_rect)
        self.screen.blit(self.red_halo_img, self.red_halo_rect)

    def show_green_total_points(self, p2_total_point):
        """Display the total green points"""
        # Points
        font_img = self.points_font.render(f"{p2_total_point}", False, 'Black')
        font_rect = font_img.get_rect(center=(1000, 510))
        # Show
        self.screen.blit(font_img, font_rect)
        self.screen.blit(self.green_halo_img, self.green_halo_rect)

    def set_timer_text(self):
        timer = pg.time.get_ticks() / 1000
        timer = dt.datetime.fromtimestamp(timer)
        text = self.font.render(f'Time   {timer.minute} : {timer.second}', False, 'Black')
        text_rect = text.get_rect(center=(self.X_POS, self.Y_POS + 35))
        self.screen.blit(text, text_rect)

    def get_players_score_per(self, p1_score: int, p2_score: int) -> tuple[float, float]:
        """"""
        total_points = p1_score + p2_score
        # Red Bar Player
        try:
            p1_points_per = p1_score / total_points
        except ZeroDivisionError:
            p1_points_per = 0
        try:
            p2_points_per = p2_score / total_points
        except ZeroDivisionError:
            p2_points_per = 0

        return p1_points_per, p2_points_per

    def show_players_score_per(self, p1_score: int, p2_score: int):
        # Get Scores percentage
        p1_score_per, p2_score_per = self.get_players_score_per(p1_score, p2_score)
        # Setup Player1
        self.set_p1_score_per(p1_score_per)
        self.set_p2_score_per(p2_score_per)

    def set_p1_score_per(self, p1_score_per: float):
        """Set the player 1 percentage score inside the bar"""
        p1_score_per_text = self.font.render(f'{p1_score_per * 100:.0f} %', False, 'White')
        p1_score_per_text_shadow = self.font.render(f'{p1_score_per * 100:.0f} %', False, 'Black')
        # Select the midleft coordinates and add 10 to the X to add margin
        coordinates = (self.rect.midleft[0] + 10, self.rect.midleft[1])
        # Move a little the text to create the effect of shadow
        coordinates_shadow = (self.rect.midleft[0] + 9, self.rect.midleft[1] + 2)
        p1_score_per_text_rect = p1_score_per_text.get_rect(midleft=coordinates)
        p1_score_per_text_rect_shadow = p1_score_per_text.get_rect(midleft=coordinates_shadow)
        # show
        self.screen.blit(p1_score_per_text_shadow, p1_score_per_text_rect_shadow)
        self.screen.blit(p1_score_per_text, p1_score_per_text_rect)

    def set_p2_score_per(self, p2_score_per: float):
        """Set the player 2 percentage score inside the bar"""
        p1_score_per_text = self.font.render(f'{p2_score_per * 100:.0f} %', False, 'White')
        p1_score_per_text_shadow = self.font.render(f'{p2_score_per * 100:.0f} %', False, 'Black')
        # Select the midrigth coordinates and add 10 to the X to add margin
        coordinates = (self.rect.midright[0] - 45, self.rect.midright[1])
        # Move a little the text to create the effect of shadow
        coordinates_shadow = (self.rect.midright[0] - 46, self.rect.midright[1] + 2)
        p1_score_per_text_rect = p1_score_per_text.get_rect(midleft=coordinates)
        p1_score_per_text_rect_shadow = p1_score_per_text.get_rect(midleft=coordinates_shadow)
        # show
        self.screen.blit(p1_score_per_text_shadow, p1_score_per_text_rect_shadow)
        self.screen.blit(p1_score_per_text, p1_score_per_text_rect)

    def update(self, p1_score: int, p2_score: int, turns: int):
        self.update_bar_size(p1_score, p2_score)
        self.show_red_bar()
        self.show_turns_text(turns)
        self.show_players_score_per(p1_score, p2_score)
        self.show_red_total_points(p1_score)
        self.show_green_total_points(p2_score)
        self.set_timer_text()
