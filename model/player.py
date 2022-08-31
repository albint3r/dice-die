# Import
# Hint Types
from dataclasses import dataclass


@dataclass
class Player:

    name: str = None

    def set_player_name(self, name: str) -> None:
        """Change the name of the player"""
        self.name = name.strip().title()
