# Imports
import os
# Hint Types
from dataclasses import dataclass
# Project Modules
from view.terminal.abstract_view import AbstractView


@dataclass
class TerminalView(AbstractView):

    def show_dice_result(self, current_player) -> None:
        print(f'Dice Result: {current_player.dice.number}')

    def show_select_target_column_error(self):
        print(f'Select correct Index Column or an empty one!')

    def show_board(self, model):
        p1_zip_cols = model.prepare_board_to_show(model.p1, reverse=True)
        p2_zip_cols = model.prepare_board_to_show(model.p2, reverse=False)

        self.single_display_board(model.p1, p1_zip_cols)
        self.single_display_board(model.p2, p2_zip_cols)

    def show_leader_board(self, leader_board: list):
        if leader_board:
            print('********************************************')
            print('              Top 10 players')
            print('********************************************')
            print(f' |   Name       |  Wins  |    Avg.Turns   |')
            print('--------------------------------------------')
            for row in leader_board:

                print(f'  {row[0]:^10}    {row[1]:^10}    {row[2]:^10.0f}  ')
            print('--------------------------------------------')
        else:
            print('Game story does not exist')

    def single_display_board(self, player, zip_cols):
        # player_cols = self.prepare_board_to_show(player, reverse)
        print('\n=====================')
        print(f'{player.player.name} Board')
        print('=====================')
        print(f'   Score   ')
        print(f' {player.points_board.points[1]} ', f' {player.points_board.points[2]} ', f' {player.points_board.points[3]} ')
        for a, b, c, d in zip_cols:
            print(f'|{a}|', f'|{b}|', f'|{c}|')
        print(f'Your total score is: {player.points_board.total_points}')

    def show_player_current_turn(self, player):
        print(f'Is turn of --> {player.player.name}')

    def show_winner(self, model):
        if model.winner_status == 0:
            player = model.p1
            player2 = model.p2
            print('\n*******************************************')
            print('Game Result:')
            print('*******************************************\n')
            print(f'\nCongratulation {player.player.name} you win with [{player.points_board.total_points}] points!!! :)')
            print(f'{player2.player.name} losse with [{player2.points_board.total_points}] points. Losers  go home, bye, bye!')
            print(f'Game Over!')
        if model.winner_status == 1:
            player = model.p2
            player2 = model.p1
            print('\n*******************************************')
            print('Game Result:')
            print('*******************************************\n')
            print(f'\nCongratulation {player.player.name} you win with [{player.points_board.total_points}] points!!! :)')
            print(f'{player2.player.name} losse with [{player2.points_board.total_points}] points. Losers  go home, bye, bye!')
            print(f'Game Over!')

        if model.winner_status == 2:
            player = model.p2
            player2 = model.p1
            print('This is a tie, this is the final score:')
            print(f'Player 1: {player.player.name} ->  [{player.points_board.total_points}]')
            print(f'Player 2: {player2.player.name} ->  [{player2.points_board.total_points}]')

    def clear_console(self):
        os.system('clear')
