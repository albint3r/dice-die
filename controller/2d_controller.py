# Import
import pygame as pg
import sys
# Views
from view.score_bar import ScoreBarView
from view.board import BoarGameView

# General Set Up
pg.init()
clock = pg.time.Clock()
screen_size = (1200, 1000)
FPS = 60
screen = pg.display.set_mode(screen_size)
active_game = True

# Score Bar
scorebar = ScoreBarView(screen)
scorebar.set_rounded()
scorebar_group = pg.sprite.GroupSingle(scorebar)
# Red Board
boar_group = pg.sprite.Group()
# Green Board
boar_group.add(BoarGameView('Red'))
boar_group.add(BoarGameView('Green'))

# Fake Data
p1_score_fake = 5
p2_score_fake = 10
turn_fake = 10
grid_fake = {1: [1, 2, 0], 2: [3, 0, 5], 3: [6, 8, 1]}

while active_game:

    screen.fill('Black')  # To refresh the black screen
    for event in pg.event.get():

        # If player click cross exit game
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    # Score Bar
    scorebar.set_shadows()
    scorebar_group.draw(screen)
    scorebar_group.update(p1_score_fake, p2_score_fake, turn_fake)
    # Red Board
    # Green Board
    boar_group.draw(screen)
    boar_group.update(screen, grid_fake)

    # Update All Game
    pg.display.update()


    clock.tick(FPS)
