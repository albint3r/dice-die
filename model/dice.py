# Imports
import random
# Hint Type
from dataclasses import dataclass, field


@dataclass
class Dice:
    """Dice object to play the game"""

    _min_max_numbers: tuple[int, int] = field(default=(1, 6), repr=False)
    number: int = None

    @property
    def min_max_numbers(self) -> tuple[int, int]:
        """ """
        return self._min_max_numbers

    def roll(self) -> None:
        """Select a random number and assign the result in the number dice"""
        self.number = random.randint(*self._min_max_numbers)

    def set_min_max_numbers(self, new_min_max: tuple[int, int]) -> None:
        """Change the min max numbers in the dice

        Parameters
        ----------
        new_min_max: tuple :
            Is a tuple with integer to specify the new min max dice values.

        Returns
        -------
        None
        """
        self._min_max_numbers = new_min_max

