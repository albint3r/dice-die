from controller.terminal.terminal_controller import TerminalController
from controller.game_controller import GameController
game_control = GameController()
# Project Modules
from database.models import db
db.base.metadata.create_all(db.engine)

if __name__ == '__main__':
    game_control.play()
