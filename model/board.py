# Imports
# Hint Types
from dataclasses import dataclass, field
# Project Modules
from model.score import PointsBoard
from model.player import Player
from model.dice import Dice


@dataclass
class Board:
    """Board Object"""

    dice: Dice = field(default_factory=Dice)
    points_board: PointsBoard = field(default_factory=PointsBoard)
    player: Player = field(default_factory=Player)
    grid: dict = field(default_factory=dict)
    is_turn: bool = field(default=False, repr=False)
    _max_column_size: int = field(default=3, repr=False)

    def __post_init__(self):
        self.create_grid()
        self.create_score_points()

    def add(self, target_column: int, dice_result: int) -> None:
        """Add a new Value to the target Column

        Parameters
        ----------
        target_column: int :
            Is the selected index column of the player Grid.
        dice_result: int :
            Is the result of the dice roll.

        Returns
        -------
        None
        """
        if not self.is_column_full(target_column):
            self.grid[target_column].append(dice_result)

    def create_grid(self) -> None:
        """Create start Game Grid BoarGame"""
        self.grid = {i: list() for i in range(1, self.max_column_size + 1)}

    def create_score_points(self) -> None:
        """Set the points attribute in the ScoreBoard"""
        self.points_board.create_points(max_columns=self.max_column_size)

    def count_total_existences(self, target_column: int, dice_result: int) -> int:
        """Count the total existences in the Column target

        Parameters
        ----------
        target_column: int :
            Is the selected index column of the player Grid.
        dice_result: int :
            Is the result of the dice roll.

        Returns
        -------
        Int
        """
        return self.grid[target_column].count(dice_result)

    def is_column_full(self, target_column: int) -> bool:
        """Return True if the Target column is full. Is full if it reaches the max_columns_size

        Parameters
        ----------
        target_column: int :
            Is the selected index column of the player Grid.

        Returns
        -------
        Bool
        """
        return len(self.grid[target_column]) == self.max_column_size

    def is_grid_full(self) -> bool:
        """Return True if the Player Grid is Full. Is full if it reaches the multiplication of the max_colum_size"""
        # Because is an Even Matrix it multiplies the max columns number by itself.
        return sum([len(col) for col in self.grid.values()]) == self.max_column_size * self.max_column_size

    @property
    def max_column_size(self) -> int:
        """Return tu max_column_size"""
        return self._max_column_size

    def remove_all_existences(self, target_column: int, dice_result: int) -> None:
        """Remove all the dice result existences in the target column

        Parameters
        ----------
        target_column: int :
            Is the selected index column of the player Grid.
        dice_result: int :
            Is the result of the dice roll.

        Returns
        -------
        None
        """
        total_existences = self.count_total_existences(target_column=target_column, dice_result=dice_result)
        for i in range(total_existences):
            self.grid[target_column].remove(dice_result)



