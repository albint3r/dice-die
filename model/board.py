# Imports
# Hint Types
from dataclasses import dataclass, field
# Project Modules
from model.score import ScoreBoard


@dataclass
class Board:

    grid: dict = None
    score: ScoreBoard = field(default_factory=ScoreBoard)
    _max_columns: int = field(default=3, repr=False)

    def __post_init__(self):
        self.create_grid()
        self.create_score_points()

    def add(self, target_column: int, dice_result: int) -> None:
        """Add a new Value to the target Column"""
        if not self.is_column_full(target_column):
            self.grid[target_column].append(dice_result)

    def create_grid(self) -> None:
        """Create start Game Grid BoarGame"""
        self.grid = {i: list() for i in range(1, self.max_columns + 1)}

    def create_score_points(self) -> None:
        """Set the points attribute in the ScoreBoard"""
        self.score.create_points(max_columns=self.max_columns)

    def count_total_existences(self, target_column: int, dice_result: int) -> int:
        """Count the total existences in the Column target"""
        return self.grid[target_column].count(dice_result)

    def is_column_full(self, target_column: int) -> bool:
        """Return True if the Column index is full"""
        return len(self.grid[target_column]) == self.max_columns

    @property
    def max_columns(self) -> int:
        return self._max_columns

    def remove_all_existences(self, target_column: int, dice_result: int) -> None:
        """Remove all the dice result existences in the target column"""
        total_existences = self.count_total_existences(target_column=target_column, dice_result=dice_result)
        for i in range(total_existences):
            self.grid[target_column].remove(dice_result)

    @staticmethod
    def remove_and_update_opponent_board(opponent_board, target_column: int, dice_result: int):
        """If the dice result exist in the target column it would remove all the dices result in the list of the
        opponent player."""
        if opponent_board.count_total_existences(target_column=target_column, dice_result=dice_result):
            opponent_board.remove_all_existences(target_column=target_column, dice_result=dice_result)
            # Update Opponent Column and total Score
            opponent_board.score.update_column_points(grid=opponent_board.grid, target_column=target_column)
            opponent_board.score.update_total_score()
