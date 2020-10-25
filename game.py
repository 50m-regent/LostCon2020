from random import randint

from const import *
from data import Data
from board import Board
from move import Move
from point import Point

class Game:
    def __init__(self, data = Data(), turn=10):
        self.data = data
        self.n_turn = turn
        self.search_directions = [
            Point(-1, -1),
            Point(0, -1),
            Point(1, -1),
            Point(-1, 0),
            Point(1, 0),
            Point(-1, 1),
            Point(0, 1),
            Point(1, 1)
        ]

        self.reset(reset_data=False)

    def reset(self, reset_data=True):
        self.move_queue = []
        self.moves = []

        if reset_data:
            self.data.reset()

        for p in self.data.agents_pos:
            self.move_queue.append(p)

        print('Game Reseted.')

    def is_in_board(self, v):
        return v.x > 0 and v.y > 0 and v.x <= self.data.board_size.x and v.y <= self.data.board_size.y

    def step(self):
        reserve = Board(self.data.board_size, all_zero=True)

        for move in self.moves:
            if self.is_in_board(move.after):
                reserve[move.after] += 1
            else:
                reserve[move.before] += 1

        self.data.agents_pos.clear()

        stop_counter = 0

        while len(self.moves) != 0:
            stop_counter += 1

            if stop_counter > self.data.agent_amount * self.data.agent_amount:
                break
            
            move = self.moves[0]
            self.moves = self.moves[1:]

            if reserve[move.after] > 1:
                self.data.agents_pos.append(move.before)
                continue

            if move.before.x < 0:
                agent_team = 1
            elif move.before.y < 0:
                agent_team = -1
            else:
                agent_team = self.data.walls_board[move.before]

            if move.move == 0:
                if self.data.agents_board[move.after] != 0 or self.data.walls_board[move.after] == -agent_team:
                    self.moves.append(move)
                    continue
                
                self.data.agents_pos.append(move.after)

                if not self.is_in_board(move.after):
                    continue
                
                if move.before.x < 0:
                    self.data.player_stack -= 1
                elif move.before.y < 0:
                    self.data.opponent_stack -= 1
                else:
                    self.data.agents_board[move.before] = 0

                self.data.agents_board[move.after] = agent_team
                self.data.walls_board[move.after] = agent_team

                if agent_team == 1:
                    self.data.player_wall_points += self.data.points_board[move.after]
                else:
                    self.data.opponent_wall_points += self.data.points_board[move.after]

            elif move.move == 1:
                if self.data.walls_board[move.after] == 0:
                    self.data.walls_board[move.after] = agent_team
                self.data.agents_pos.append(move.before)

            else:
                if self.data.agents_board[move.after] != 0:
                    self.moves.append(move)
                    continue

                self.data.walls_board[move.after] = 0
                self.data.agents_pos.append(move.before)
        
        while len(self.moves) != 0:
            move = self.moves[0]
            self.moves = self.moves[1:]

            self.data.agents_pos.append(move.before)

        self.data.turn += 1
        self.calculate_score()

    def sanitize(self, filter, visited, now, team):
        filter[now] = 1

        for d in self.search_directions:
            if \
                now.x + d.x >= 0 and \
                now.y + d.y >= 0 and \
                now.x + d.x <= self.data.board_size.x + 1 and \
                now.y + d.y <= self.data.board_size.y + 1 and \
                not visited[Point(now.x + d.x, now.y + d.y)] and \
                self.data.walls_board[now] != team \
            :
                visited[Point(now.x + d.x, now.y + d.y)] = 1
                self.sanitize(filter, visited, Point(now.x + d.x, now.y + d.y), team)

    def bfs(self, team):
        filter  =  Board(self.data.board_size, all_zero=True)
        visited =  Board(self.data.board_size, all_zero=True)

        self.sanitize(filter, visited, Point(0, 0), team)

        score = 0
        
        for x in range(1, self.data.board_size.x + 1):
            for y in range(1, self.data.board_size.y + 1):
                if not filter[Point(x, y)]:
                    adjacent_wall = 0
                    for d in self.search_directions:
                        if self.data.walls_board[Point(x + d.x, y + d.y)] == team:
                            adjacent_wall += 1

                    if adjacent_wall < 3:
                        continue

                    q = []
                    if \
					    self.is_in_board(Point(x, y)) and \
					    not visited[Point(x, y)] and \
					    not filter[Point(x, y)] and \
					    self.data.walls_board[Point(x, y)] == 0 \
                    :
                        q.append(Point(x, y))
                        visited[Point(x, y)] = 1                

                    while len(q) != 0:
                        now = q[0]
                        q   = q[1:]

                        if abs(self.data.walls_board[now]) != 1:
                            self.data.areas_board[now] = team
                        else:
                            data.areas_board[now] = 0

                        for d in self.search_directions:
                            if (
                                self.is_in_board(Point(now.x + d.x, now.y + d.y)) and
                                not visited[Point(now.x + d.x, now.y + d.y)] and
                                not filter[Point(now.x + d.x, now.y + d.y)] and
                                self.data.walls_board[Point(now.x + d.x, now.y + d.y)] == 0
                            ):
                                q.append(Point(now.x + d.x, now.y + d.y))
                                visited[Point(now.x + d.x, now.y + d.y)] = 1

        return score

    def calculate_score(self):
        self.data.player_area_points = self.bfs(1)
        self.data.player_area_points = self.bfs(-1)
        
        for x in range(1, self.data.board_size.x + 1):
           for y in range(1, self.data.board_size.y + 1):
               if self.data.areas_board[Point(x, y)] == 1:
                   self.data.player_area_points += abs(self.data.points_board[Point(x, y)])
               if self.data.areas_board[Point(x, y)] == -1:
                   self.data.opponent_area_points += abs(self.data.points_board[Point(x, y)])

    def make_random_move(self):
        target = self.move_queue[0]

        nx, ny = 0, 0
        if target.x < 0 or target.y < 0:
            nx = randint(1, self.data.board_size.x)
            ny = randint(1, self.data.board_size.y)
        else:
            nx = target.x + randint(-1, 1)
            ny = target.y + randint(-1, 1)

        while not self.is_in_board(Point(nx, ny)):
            if target.x < 0 or target.y < 0:
                nx = randint(1, self.data.board_size.x)
                ny = randint(1, self.data.board_size.y)
            else:
                nx = target.x + randint(-1, 1)
                ny = target.y + randint(-1, 1)

        self.moves.append(Move(
            target,
            Point(nx, ny),
            "move"
        ))
        self.move_queue = self.move_queue[1:]

    def progress(self):
        if self.data.turn > self.n_turn:
            print('Game Finished.')
            self.reset()
            return False

        if len(self.move_queue) == 0:
            self.step()

            for p in self.data.agents_pos:
                self.move_queue.append(p)

            return True
        else:
            self.make_random_move()
            return False