from controller.terminal.terminal_controller import TerminalController
from controller.game_controller import GameController
game_control = GameController()
# Project Modules
from database.models import db
db.base.metadata.create_all(db.engine)

if __name__ == '__main__':
    game_control.model.p1.player.name = 'Tobe'
    game_control.model.p2.player.name = 'Viper'

    game_control.play()
