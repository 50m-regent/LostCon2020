from const import *
from board import Board
from point import Point
from random import randint

class Data:
    def __init__(self):
        self.board_size     = self.generate_random_size()
        self.points_board   = Board(self.board_size)
        self.agents_board   = Board(self.board_size, all_zero=True)
        self.walls_board    = Board(self.board_size, all_zero=True)
        self.areas_board    = Board(self.board_size, all_zero=True)

        tmp = self.generate_random_agent_amount()
        self.player_stack   = tmp
        self.opponent_stack = tmp
        self.agent_amount   = tmp

        self.agents_pos = []
        self.turn = 1

        self.player_wall_points   = 0
        self.opponent_wall_points = 0

        self.player_area_points   = 0
        self.opponent_area_points = 0

        for i in range(self.agent_amount):
            self.agents_pos.append(Point(-1 ,0))
            self.agents_pos.append(Point(0, -1))

    def reset(self):
        self.__init__()

    def generate_random_size(self):
        return Point(
            randint(BOARD_SIZE_MIN, BOARD_SIZE_MAX),
            randint(BOARD_SIZE_MIN, BOARD_SIZE_MAX)
        )

    def generate_random_agent_amount(self):
        capped_min = int(min(AGENT_AMOUNT_MAX, AGENT_AMOUNT_MIN * (self.board_size.x + self.board_size.y) / (2 * BOARD_SIZE_MIN)))
        capped_max = int(max(AGENT_AMOUNT_MIN, AGENT_AMOUNT_MAX * (self.board_size.x + self.board_size.y) / (2 * BOARD_SIZE_MAX)))
        return capped_min + randint(0, capped_max - capped_min)

    @staticmethod
    def from_json(json):
        data = Data()
        data.board_size = Point.from_json(json['board_size'])
        data.points_board = Board.from_json(json['points_board'])
        data.agents_board = Board.from_json(json['agents_board'])
        data.walls_board = Board.from_json(json['walls_board'])
        data.areas_board = Board.from_json(json['areas_board'])
        data.player_stack = json['player_stack']
        data.opponent_stack = json['opponent_stack']
        data.agent_amount = json['agent_amount']
        data.agents_pos = [Point.from_json(p) for p in json['agents_pos']]
        data.turn = json['turn']
        data.player_wall_points = json['player_wall_points']
        data.opponent_wall_points = json['opponent_wall_points']
        data.player_area_points = json['player_area_points']
        data.opponent_area_points = json['opponent_area_points']

        return data
    
    def to_json(self):
        return {
            'board_size':           self.board_size.to_json(),
            'points_board':         self.points_board.to_json(),
            'agents_board':         self.agents_board.to_json(),
            'walls_board':          self.walls_board.to_json(),
            'areas_board':          self.areas_board.to_json(),
            'player_stack':         self.player_stack,
            'opponent_stack':       self.opponent_stack,
            'agent_amount':         self.agent_amount,
            'agents_pos':           [p.to_json() for p in self.agents_pos],
            'turn':                 self.turn,
            'player_wall_points':   self.player_wall_points,
            'opponent_wall_points': self.opponent_wall_points,
            'player_area_points':   self.player_area_points,
            'opponent_area_points': self.opponent_area_points,
        }