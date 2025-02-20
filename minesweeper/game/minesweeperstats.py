import math
from typing import List

from minesweeper.game.minesweepergame import MinesweeperGame


class MinesweeperStats:
    game: MinesweeperGame
    _traversed_board: List[List[bool]]  # needs to be reinitialised as all 'False' in order to count 3bv properly
    tbv: int
    tbv_per_second: float
    ios: float
    rqp: float

    def __init__(self, game: MinesweeperGame):
        self.game = game
        self._traversed_board = [[False] * game.width for _ in range(game.height)]
        self.tbv = self.calculate_3bv()
        seconds = game.time_spent/1000
        self.tbv_per_second = self.tbv/seconds
        self.ios = math.log(self.tbv) / math.log(seconds)
        self.rqp = seconds / self.tbv_per_second

    def open_cells_recursively(self, y, x):
        """Used for counting blank blobs in the minesweeper board
        This method opens cell under logic_board[y][x] recursively and marks them as traversed.
        Used for marking blank blobs in the minesweeper board by adding them
        to the traversed matrix, along with their numbered extremities.


        Args:
            y: cell height coordinate
            x: cell width coordinate

        Returns:
            None

        """
        if self._traversed_board[y][x]:
            return

        self._traversed_board[y][x] = True

        if self.game.logic_board[y][x] > 0:
            return

        for dy in range(y - 1, y + 1 + 1):
            if not 0 <= dy < self.game.height:
                continue

            for dx in range(x - 1, x + 1 + 1):
                if not 0 <= dx < self.game.width:
                    continue

                if dy == y and dx == x:
                    continue

                self.open_cells_recursively(dy, dx)

    def calculate_3bv(self):
        """Calculates 3bv statistic by first counting blank blobs, and then
        every cell that needs to be clicked individually in order to win the game

        Returns:
            tbv (int): the 3bv statistic for the board
        """
        tbv = 0

        for y in range(self.game.height):
            for x in range(self.game.width):
                if (not self._traversed_board[y][x]) and self.game.logic_board[y][x] == 0:
                    self.open_cells_recursively(y, x)
                    tbv += 1

        for y in range(self.game.height):
            for x in range(self.game.width):
                if (not self._traversed_board[y][x]) and self.game.logic_board[y][x] > 0:
                    tbv += 1

        return tbv
