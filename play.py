from controller.terminal.terminal_controller import TerminalController
from controller.game_controller import GameController
game_control = GameController()

if __name__ == '__main__':
    game_control.model.p1.player.name = 'Tobe'
    game_control.model.p2.player.name = 'Jp'

    game_control.play()
