# Imports
import os
# Hint Types
from dataclasses import dataclass, field
import sqlalchemy  # Used to the hint types of the attributes
# DataBase
from database.models import GameResult, GridsResult
from database.database_game import DataBaseGame


@dataclass
class PointsBoard:

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
class ScoreMatch:
    result_tb: GameResult = field(default_factory=GameResult)
    grid_tb: GridsResult = field(default_factory=GridsResult)
    db: DataBaseGame = field(default_factory=DataBaseGame)
    total_turns: int = 0

    def plus_one_total_turn(self) -> None:
        """Add one each turn to follow the turns counter"""
        self.total_turns += 1

    def get_last_10_games(self) -> list:
        """Return the last 10 games results"""
        return self.db.session.query(GameResult).limit(10).all()

    def get_leader_score(self) -> list[tuple]:
        """Return the Leader Score"""
        with self.db.engine.connect() as con:
            query = """
            SELECT winner_name, COUNT(winner_name), AVG(total_turns) AS wins  
            FROM GameResult 
            GROUP BY winner_name
            ORDER BY COUNT(winner_name) DESC
            LIMIT 10
            """
            result = con.execute(query)
            return [row for row in result]


