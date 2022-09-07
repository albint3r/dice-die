from controller.terminal.terminal_controller import TerminalController
from controller.game_controller import GameController
game_control = GameController()

if __name__ == '__main__':
    game_control.model.p1.player.name = 'Martin'
    game_control.model.p2.player.name = 'Viper'

    game_control.play()
