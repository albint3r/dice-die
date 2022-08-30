# Imports
import os
# Hint Types
from dataclasses import dataclass, field
import sqlalchemy  # Used to the hint types of the attributes
# DataBase
from database.models import GameResult


@dataclass
class ScoreBoard:
    points: dict = field(default_factory=dict)
    total_points: int = 0

    def create_points(self, max_columns: int):
        self.points = {i: 0 for i in range(1, max_columns + 1)}

    def update_column_points(self, grid: dict, target_column: int):
        """Calculate the Points Score in the Column Target"""
        unique_numbers = set(grid[target_column])
        dice_count = {num: grid[target_column].count(num) for num in unique_numbers}
        self.points[target_column] = sum([(count * num) * count for num, count in dice_count.items()])

    def update_total_score(self):
        """Calculate the Points Score in the Column Target"""
        self.total_points = sum(self.points.values())


@dataclass
class ScoreGame:

    game_result: GameResult = field(default_factory=GameResult)
