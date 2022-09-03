# Import
import random
from itertools import zip_longest
# Hint Type
from dataclasses import dataclass, field
from typing import Any, Generator

# Project Modules
from model.board import Board
from model.score import ScoreMatch


@dataclass
class GameModel:
    """Game Model: Serve to give all the components to the controller to play the game"""
    p1: Board = field(default_factory=Board)
    p2: Board = field(default_factory=Board)
    score_match: ScoreMatch = field(default_factory=ScoreMatch, repr=False)
    winner_status: int | None = None
    last_turn_grids: list | None = None  # Is the last turn board grid result of both players.
    changes_state: dict | None = None

    def __post_init__(self):
        # Init a last
        self.last_turn_grids = [{1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0]},  # P1
                                {1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0]}]  # P2

    @staticmethod
    def change_player_turn(turn: int) -> int:
        """Change the player turn"""
        # If is 1 select the player1 else select player2
        return 0 if turn else 1

    @staticmethod
    def is_game_over(current_player) -> bool:
        """Return True if the game is over"""
        return False if current_player.is_grid_full() else True

    @staticmethod
    def fill_missing_dice_results(player: Board, fill_value: int = 0):
        """Fill the NaN values with Zero"""
        for i in range(1, player.max_column_size + 1):
            if not player.is_column_full(i):
                player.grid.get(i).append(fill_value)
                GameModel.fill_missing_dice_results(player)

    @staticmethod
    def copy_fill_missing(grid: dict, reverse=False, fill_value: int = 0) -> dict:
        """Create a Copy of the Player Grid and fill all the missing values.
        This helps to display the grid result in the 2D version.
        """
        max_grid_range = 3
        # Copy new dict to avoid errors
        copy = grid.copy()
        # Copy all the List to avoid errors
        for i in range(1, max_grid_range + 1):
            copy[i] = grid[i].copy()
        # Fill missing values
        for i in range(1, max_grid_range + 1):
            col = copy.get(i)
            total_missing_vals = max_grid_range - len(col)
            if total_missing_vals:
                for ii in range(total_missing_vals):
                    col.append(fill_value)

        if reverse:
            copy[1] = copy[1][::-1]
            copy[2] = copy[2][::-1]
            copy[3] = copy[3][::-1]

        return copy

    @staticmethod
    def prepare_board_to_show(player: Board, reverse: bool = False) -> zip | zip_longest:
        """Organize and fill missing values of the BoardGrid to be displayed

        Parameters
        ----------
        player : Board:
            This is a Board Object / Player that would be applied the prepared board function
            
        reverse: bool :
            If this is True it will apply the Revers method, that revers the column values to be displayed.
             (Default value = False)

        Returns
        -------
        zip | zip_longest
        """

        # This Generator have a ranges between 1 and the max_column_size plus 2
        # This helps to create a fake/hide Column. This helps to fill the grid columns values with 0
        # Otherwise this would be uneven columns with variable total of values inside each column
        grid = (player.grid[i] if player.grid.get(i) is not None else list(range(1, player.max_column_size + 1)) \
                for i in range(1, player.max_column_size + 2))

        zip_grid = zip_longest(*grid, fillvalue=0)

        if reverse:
            return GameModel.reverse_grid(zip_grid)

        return zip_grid

    @staticmethod
    def reverse_grid(zip_grid: zip_longest) -> zip:
        """Display the numbers on the grid bottom to top

        Parameters
        ----------
        zip_grid : zip_longest:
            Is a zip object tha contain all the columns to be reversed.

        Returns
        -------
        zip
        """
        col1, col2, col3, col4 = [], [], [], []

        for a, b, c, d, in zip_grid:
            col1.append(a)
            col2.append(b)
            col3.append(c)
            col4.append(d)

        return zip(col1[::-1], col2[::-1], col3[::-1], col4[::-1])

    @staticmethod
    def remove_and_update_opponent_board(opponent: Board, target_column: int, dice_result: int) -> None:
        """If the dice result exist in the target column it would remove all the dices result in the list of the
        opponent player.

        Parameters
        -----------
        opponent: Board :
            Is a Board objet that represent the opponent player. If player1 opponent would be player2, If player 2
            opponent would be player 1
            
        target_column: int :
            Is the selected index column of the player Grid.
            
        dice_result: int :
            Is the result of the dice roll.
            

        Returns
        -------
        None
        """
        # If is one or more existences it will remove all the values in the column
        if opponent.count_total_existences(target_column=target_column, dice_result=dice_result):
            opponent.remove_all_existences(target_column=target_column, dice_result=dice_result)
            # Update Opponent Column and total Score
            opponent.points_board.update_column_points(grid=opponent.grid, target_column=target_column)
            opponent.points_board.update_total_score()

    def select_player_start(self) -> tuple[Board, Board]:
        """Simulate a coin toss to select which player starts
        This change the is_turn attribute to True if the player start, but this only works in the 2D version.
        """
        coin_toss = random.randint(0, 1)
        players_order = (self.p1, self.p2) if coin_toss else (self.p2, self.p1)
        players_order[0].is_turn = True
        return players_order

    @staticmethod
    def select_opponent(players: tuple, turn: int) -> Board:
        """Select the Opponent of the current player"""
        # if the turn is 0 opponent is player 2, else opponent is player 1
        return players[1] if not turn else players[0]

    def select_winner(self) -> None:
        """Select the winner of the game by the high score."""
        if self.p1.points_board.total_points > self.p2.points_board.total_points:
            self.winner_status = 0  # Player 1 Win the game
        elif self.p2.points_board.total_points > self.p1.points_board.total_points:
            self.winner_status = 1  # Player 2 win the game
        else:
            self.winner_status = 2  # Tie

    def save_game_result(self) -> None:
        """Save the PointsBoar Game Result"""
        self.score_match.result_tb.set_result_game(p1_name=self.p1.player.name,
                                                   p2_name=self.p2.player.name,
                                                   p1_score=self.p1.points_board.total_points,
                                                   p2_score=self.p2.points_board.total_points,
                                                   win=self.winner_status,
                                                   winner_name=self.p2.player.name if self.winner_status else self.p1.player.name,
                                                   total_turns=self.score_match.total_turns)

        self.score_match.result_tb.save()

    def save_game_grid(self) -> None:
        """Save the Grid Boards of the match"""
        self.score_match.grid_tb.set_result_grid(
            # Player 1
            # Col1
            p1_row0_col1=self.p1.grid.get(1)[0],
            p1_row1_col1=self.p1.grid.get(1)[1],
            p1_row2_col1=self.p1.grid.get(1)[2],
            # Col2
            p1_row0_col2=self.p1.grid.get(2)[0],
            p1_row1_col2=self.p1.grid.get(2)[1],
            p1_row2_col2=self.p1.grid.get(2)[2],
            # Col3
            p1_row0_col3=self.p1.grid.get(3)[0],
            p1_row1_col3=self.p1.grid.get(3)[1],
            p1_row2_col3=self.p1.grid.get(3)[2],
            # Player 2
            # Col1
            p2_row0_col1=self.p2.grid.get(1)[0],
            p2_row1_col1=self.p2.grid.get(1)[1],
            p2_row2_col1=self.p2.grid.get(1)[2],
            # Col2
            p2_row0_col2=self.p2.grid.get(2)[0],
            p2_row1_col2=self.p2.grid.get(2)[1],
            p2_row2_col2=self.p2.grid.get(2)[2],
            # Col3
            p2_row0_col3=self.p2.grid.get(3)[0],
            p2_row1_col3=self.p2.grid.get(3)[1],
            p2_row2_col3=self.p2.grid.get(3)[2],
            match_id=self.score_match.result_tb.id,
        )

        self.score_match.grid_tb.save()

    def create_last_turn_grids(self) -> list:
        return [self.copy_fill_missing(grid) for grid in (self.p1.grid, self.p2.grid)]

    def get_removed_dices_player(self, echo: bool = False) -> dict:
        # Validate if exist the last turn grid
        detected_changes = {1: None, 2: None}
        new_copies = self.create_last_turn_grids()
        player_counter = 1  # This helps to organize the order of the players changes.
        if self.last_turn_grids:
            # Extract the game of player 1 and 2, and check each column for changes.
            for old_copy, new_copy in zip(self.last_turn_grids, new_copies):
                # Select by index each column
                for i in range(1, 4):
                    # Check Tru if note changes between the new and the old copy.
                    if not old_copy[i] == new_copy[i]:
                        # Leave this prints to watch all the proces
                        if echo:
                            print(f'\n**** Player {player_counter} ********')
                            print('old', old_copy[i])
                            print('new', new_copy[i])
                        changes_list = self.mark_removed_dices(new_copy[i], old_copy[i])
                        detected_changes[player_counter] = {i: changes_list}

                player_counter += 1  # Change player

        # Assign values
        self.last_turn_grids = new_copies
        if echo:
            print(detected_changes)
            print(f'**********************************')
        return detected_changes

    @staticmethod
    def mark_removed_dices(col_new_copy, col_old_copy) -> list:
        """Mark with TRUE the removed dices in a Column opponent.
        This is a True/False list in the same index order of the target Column.
        This would help to iterate on each boolean and apply an animation when the dice is destroyed.
        """

        # Check the differences and select the only number that expect the game.
        num_missing = set(col_old_copy).difference(set(col_new_copy))
        num_missing = list(num_missing)[0] if num_missing else 0
        # Find index of the missing values if there are not 0
        if num_missing:
            indexes_missing_num = [True if num == num_missing else False for i, num in enumerate(col_old_copy)]
            return indexes_missing_num
