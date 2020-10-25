from random import randint

from const import *
from point import Point

class Board:
    def __init__(self, size, all_zero=False):
        self.board = [[0 if all_zero else randint(CELL_POINT_MIN, CELL_POINT_MAX) for x in range(size.x + 2)] for y in range(size.y + 2)]

    def __getitem__(self, point):
        return self.board[point.y][point.x]

    def __setitem__(self, point, val):
        self.board[point.y][point.x] = val

    def __str__(self):
        string = ''
        for row in self.board:
            for cell in row:
                string += '{:4}'.format(cell)
            string += '\n'

        return string

    @staticmethod
    def from_json(json):
        size = Point(len(json), len(json[0]))
        board = Board(size)
        board.board = json
        return board

    def to_json(self):
        return self.board