# Import
import re
# Hint Type
# Project Modules
from controller.terminal.abstract_controller import AbstractController
from view.terminal.terminal_view import TerminalView


class TerminalController(AbstractController):

    def __init__(self):
        self.view = TerminalView()
        super().__init__()

    def set_players_names(self):
        self.model.p1.player.name = input('Select the name of player1: ').title()
        self.model.p2.player.name = input('Select the name of player2: ').title()

    def start_new_game(self) -> None:
        flag = True
        while flag:
            request = input("Type 'y' or 'n' to start o finish the game:")
            if request == 'y':
                # This method need to create another Class Object
                # If this not occur it will display the last game
                ctrl = TerminalController()
                ctrl.play()

            if request == 'n':
                print('Game Finished')
                flag = False

    def set_target_column(self, current_player, view_msg):
        """Assign an integer value to the target column attribute.
         This helps to add the dice result to the column in the grid."""
        flag = True

        while flag:
            request = input('Select target column: ').strip()
            if re.search(r'[1-3]', request) and int(request) < current_player.max_column_size + 1:
                self.target_column = int(request)
                if not current_player.is_column_full(self.target_column):
                    flag = False
            else:
                view_msg()

    def play(self):
        # Show leader board before start the game
        self.view.show_leader_board(self.model.score_match.get_leader_score())
        # Select contenders names
        self.set_players_names()
        # Define which player starts first
        players = self.model.select_player_start()
        # Game Start loop
        while self.game_on:
            # Assign player turn
            current_player = players[self.turn]
            self.view.show_player_current_turn(current_player)
            # Roll dice
            current_player.dice.roll()
            self.view.show_dice_result(current_player)
            self.view.show_board(self.model)
            # Where you want to put the dice result?
            self.set_target_column(current_player, self.view.show_select_target_column_error)
            current_player.add(self.target_column, current_player.dice.number)
            current_player.points_board.update_column_points(current_player.grid, self.target_column)
            current_player.points_board.update_total_score()
            # Opponent have the dice result in the same target Colum?
            opponent = self.model.select_opponent(players, self.turn)
            self.model.remove_and_update_opponent_board(opponent, self.target_column, current_player.dice.number)
            self.model.score_match.plus_one_total_turn()
            self.view.clear_console()
            # Is Game Over or next player?
            self.game_on = self.model.is_game_over(current_player)
            self.turn = self.model.change_player_turn(self.turn)
            # removed_dices_index = self.model.get_removed_dices_player(echo=True)  # This is used to test only
            self.model.copy_fill_missing(self.model.p1.grid, True)

        # Win Menu
        self.model.select_winner()
        self.view.show_winner(self.model)
        self.model.fill_missing_dice_results(self.model.p1)
        self.model.fill_missing_dice_results(self.model.p2)

        self.model.save_game_result()
        self.model.save_game_grid()
