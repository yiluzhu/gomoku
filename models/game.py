from ai.brain import Brain
from constants import BOARD_SIZE, NUM_IN_A_ROW


class Piece:
    def __init__(self, count):
        """Black always moves first
        Use numbers to represent colors. 1 for black pieces, 0 for white pieces
        :param count: count the number of turns, starts with 1 by black move
        """
        self.id = count
        self.color = count % 2


class GameModel:
    def __init__(self):
        """Initialize N * N board. If a point has no piece on it, the value is None"""
        self.count = 0
        self.board = [[None for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.ai = Brain(self.board)
        self.latest_move = None
        self.versus_mode = None

    def reset(self):
        self.__init__()
        print('Restart game.')

    def ai_move(self, x=None, y=None):
        if not x or not y:
            x, y = self.ai.move()
        return self.on_click(x, y)

    def set_versus_mode(self, mode):
        self.versus_mode = mode

    def on_click(self, x, y):
        """When a player clicked point (x, y)"""
        if self.has_piece(x, y):
            piece_color = None
            win = False
        else:
            self.play_a_piece(x, y)
            piece_color = self.get_latest_piece_color()
            win = self.check_winning()

        return {'piece_color': piece_color, 'win': win, 'x': x, 'y': y}

    def has_piece(self, x, y):
        """Is there a piece on point (x, y)?"""
        return 0 <= x <= BOARD_SIZE - 1 and 0 <= y <= BOARD_SIZE - 1 and self.board[x][y]

    def play_a_piece(self, x, y):
        """Play a piece on board at (x, y)
        :param x: row index
        :param y: col index
        :return: 
        """
        self.count += 1
        self.latest_move = (x, y)
        self.board[x][y] = Piece(self.count)
        print('black' if self.count % 2 == 1 else 'white', '< x:', x, ', y:', y,'>')

    def get_latest_piece_color(self):
        """Who made the latest move"""
        return 'black' if self.count % 2 == 1 else 'white'

    def is_same_color(self, x, y):
        """Check if a point has a piece and that piece is the same color as the latest one"""
        return self.has_piece(x, y) and self.board[x][y].color == self.count % 2

    def check_winning(self):
        """Check if the latest piece makes 5-in-a-row"""
        x, y = self.latest_move
        return self.check_horizontal(x, y) or self.check_vertical(x, y) or self.check_top_left_to_bottom_right(x, y) or self.check_top_right_to_bottom_left(x, y)

    def check_horizontal(self, x, y):
        """Given a point, check the horizontal direction from left to right, to see if there is any 5-in-a-row. 
        :param x: row index
        :param y: col index
        :return: True if a 5-in-a-row situation is found, otherwise False
        """
        # return (self.is_same_color(x, y - 4) and self.is_same_color(x, y - 3) and self.is_same_color(x, y - 2) and self.is_same_color(x, y - 1)) or \
        #        (self.is_same_color(x, y - 3) and self.is_same_color(x, y - 2) and self.is_same_color(x, y - 1) and self.is_same_color(x, y + 1)) or \
        #        (self.is_same_color(x, y - 2) and self.is_same_color(x, y - 1) and self.is_same_color(x, y + 1) and self.is_same_color(x, y + 2)) or \
        #        (self.is_same_color(x, y - 1) and self.is_same_color(x, y + 1) and self.is_same_color(x, y + 2) and self.is_same_color(x, y + 3)) or \
        #        (self.is_same_color(x, y + 1) and self.is_same_color(x, y + 2) and self.is_same_color(x, y + 3) and self.is_same_color(x, y + 4))

        return any(all(self.is_same_color(x, y + i) for i in range(j, NUM_IN_A_ROW + j) if i) for j in range(1 - NUM_IN_A_ROW, 1))

    def check_vertical(self, x, y):
        """Given a point, check the vertical direction from top to bottom, to see if there is any 5-in-a-row. 
        :param x: row index
        :param y: col index
        :return: True if a 5-in-a-row situation is found, otherwise False
        """
        # return (self.is_same_color(x - 4, y) and self.is_same_color(x - 3, y) and self.is_same_color(x - 2, y) and self.is_same_color(x - 1, y)) or \
        #        (self.is_same_color(x - 3, y) and self.is_same_color(x - 2, y) and self.is_same_color(x - 1, y) and self.is_same_color(x + 1, y)) or \
        #        (self.is_same_color(x - 2, y) and self.is_same_color(x - 1, y) and self.is_same_color(x + 1, y) and self.is_same_color(x + 2, y)) or \
        #        (self.is_same_color(x - 1, y) and self.is_same_color(x + 1, y) and self.is_same_color(x + 2, y) and self.is_same_color(x + 3, y)) or \
        #        (self.is_same_color(x + 1, y) and self.is_same_color(x + 2, y) and self.is_same_color(x + 3, y) and self.is_same_color(x + 4, y))

        return any(all(self.is_same_color(x + i, y) for i in range(j, NUM_IN_A_ROW + j) if i) for j in range(1 - NUM_IN_A_ROW, 1))

    def check_top_left_to_bottom_right(self, x, y):
        """Given a point, check the diagonal direction from top left to bottom right, to see if there is any 5-in-a-row. 
        :param x: row index
        :param y: col index
        :return: True if a 5-in-a-row situation is found, otherwise False
        """
        # readable algorithm:
        # return (self.is_same_color(x - 4, y - 4) and self.is_same_color(x - 3, y - 3) and self.is_same_color(x - 2, y - 2) and self.is_same_color(x - 1, y - 1)) or \
        #        (self.is_same_color(x - 3, y - 3) and self.is_same_color(x - 2, y - 2) and self.is_same_color(x - 1, y - 1) and self.is_same_color(x + 1, y + 1)) or \
        #        (self.is_same_color(x - 2, y - 2) and self.is_same_color(x - 1, y - 1) and self.is_same_color(x + 1, y + 1) and self.is_same_color(x + 2, y + 2)) or \
        #        (self.is_same_color(x - 1, y - 1) and self.is_same_color(x + 1, y + 1) and self.is_same_color(x + 2, y + 2) and self.is_same_color(x + 3, y + 3)) or \
        #        (self.is_same_color(x + 1, y + 1) and self.is_same_color(x + 2, y + 2) and self.is_same_color(x + 3, y + 3) and self.is_same_color(x + 4, y + 4))

        return any(all(self.is_same_color(x + i, y + i) for i in range(j, NUM_IN_A_ROW + j) if i) for j in range(1 - NUM_IN_A_ROW, 1))

    def check_top_right_to_bottom_left(self, x, y):
        """Given a point, check the diagonal direction from top right to bottom left, to see if there is any 5-in-a-row. 
        :param x: row index
        :param y: col index
        :return: True if a 5-in-a-row situation is found, otherwise False
        """
        # return (self.is_same_color(x - 4, y + 4) and self.is_same_color(x - 3, y + 3) and self.is_same_color(x - 2, y + 2) and self.is_same_color(x - 1, y + 1)) or \
        #        (self.is_same_color(x - 3, y + 3) and self.is_same_color(x - 2, y + 2) and self.is_same_color(x - 1, y + 1) and self.is_same_color(x + 1, y - 1)) or \
        #        (self.is_same_color(x - 2, y + 2) and self.is_same_color(x - 1, y + 1) and self.is_same_color(x + 1, y - 1) and self.is_same_color(x + 2, y - 2)) or \
        #        (self.is_same_color(x - 1, y + 1) and self.is_same_color(x + 1, y - 1) and self.is_same_color(x + 2, y - 2) and self.is_same_color(x + 3, y - 3)) or \
        #        (self.is_same_color(x + 1, y - 1) and self.is_same_color(x + 2, y - 2) and self.is_same_color(x + 3, y - 3) and self.is_same_color(x + 4, y - 4))

        return any(all(self.is_same_color(x - i, y + i) for i in range(j, NUM_IN_A_ROW + j) if i) for j in range(1 - NUM_IN_A_ROW, 1))
