# Imports
from abc import ABC, abstractmethod
# Hint Types
from dataclasses import dataclass


@dataclass
class AbstractView(ABC):

    @abstractmethod
    def show_dice_result(self, current_player):
        pass

    @abstractmethod
    def show_select_target_column_error(self):
        pass

    @abstractmethod
    def show_player_current_turn(self):
        pass

    @abstractmethod
    def show_board(self):
        pass

    @abstractmethod
    def show_winner(self, winner: int):
        pass

    @abstractmethod
    def show_leader_board(self, leader_board_: list):
        pass

