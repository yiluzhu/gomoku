from random import randint
from constants import BOARD_SIZE


class Brain(object):
    def __init__(self, board):
        self.board = board

    def move(self):
        while True:
            x = randint(0, BOARD_SIZE - 1)
            y = randint(0, BOARD_SIZE - 1)
            if not self.has_piece(x, y):
                break
        return x, y

    def has_piece(self, x, y):
        """Is there a piece on point (x, y)?"""
        return 0 <= x <= BOARD_SIZE - 1 and 0 <= y <= BOARD_SIZE - 1 and self.board[x][y]
