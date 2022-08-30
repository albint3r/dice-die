# Imports
import random
# Hint Type
from dataclasses import dataclass


@dataclass
class Dice:

    _min_max_numbers: tuple[int, int] = (1, 6)
    number: int = None

    @property
    def min_max_numbers(self):
        return self._min_max_numbers

    def roll(self):
        """Select a random number and assign the result in the number dice"""
        self.number = random.randint(*self._min_max_numbers)

    def set_min_max_numbers(self, new_min_max: tuple):
        """Change the min max numbers in the dice"""
        self._min_max_numbers = new_min_max

