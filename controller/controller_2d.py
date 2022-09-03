# Import
import pygame as pg
import sys
# Views
from view.score_bar import ScoreBarView
from view.board import BoarGameView
# Model
from model.game_engine import GameModel

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
grid1_fake = {1: [1, 2, 3], 2: [3, 7, 5], 3: [6, 2, 1]}
grid2_fake = {1: [2, 2, 0], 2: [3, 6, 5], 3: [1, 2, 0]}
grid1_points_fake = {1: 10, 2: 20, 3: 3}
grid2_points_fake = {1: 0, 2: 10, 3: 3}
removed_dices_player_event_fake = {1: {3: [False, True, False]}, 2: {3: None}}


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

    # Boards
    boar_group.draw(screen)
    boar_group.update(screen, grid1_fake, grid2_fake, grid1_points_fake, grid2_points_fake,
                      removed_dices_player_event_fake)

    # Update All Game
    pg.display.update()

    clock.tick(FPS)
