# Import
from abc import ABC, abstractmethod
# Hint Type
from dataclasses import dataclass, field
# Project Modules
from model.game_engine import GameModel


@dataclass
class AbstractController(ABC):

    model: GameModel = field(default_factory=GameModel)
    target_column: int = None
    turn: int = 0  # p1 = 0 or p2 = 1
    game_on: bool = True

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def set_players_names(self):
        pass

    def set_target_column(self, current_player):
        """Assign an integer value to the target column attribute.
         This helps to add the dice result to the column in the grid."""
        pass

    @abstractmethod
    def start_new_game(self):
        pass



