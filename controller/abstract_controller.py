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

    def select_opponent(self, players: tuple):
        """Select the Opponent of the current player"""
        # if the turn is 0 select opponent is player 2, else opponent is player 1
        return players[1] if not self.turn else players[0]

    def is_game_over(self, current_player) -> None:
        """Return True if the game is over"""
        self.game_on = False if current_player.is_grid_full() else True

    def change_player_turn(self) -> None:
        """Change the player turn"""
        # If is 1 select the player1 else select player2
        self.turn = 0 if self.turn else 1
