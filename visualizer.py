import threading
from requests import get
from tkinter import Tk, Canvas, Button
from json import loads
import sys

from point import Point
from data import Data
from game import Game

WIN_WIDTH  = 1600
WIN_HEIGHT = 900
WIN_MARGIN = 50

CELL_MARGIN = 5

AGENT_COLORS = [
    'red',
    'gray90',
    'blue'
]
WALL_COLORS = [
    'tomato',
    'gray90',
    'DeepSkyBlue3'
]
AREA_COLORS = [
    'salmon',
    'gray90',
    'SkyBlue1'
]

class Visualizer():
    def __init__(self, game=None):
        if game == None:
            self.game = Game()
            self.is_online = True
        else:
            self.game = game
            self.is_online = False
        
        self.app = Tk()
        self.app.title('Procon')
        self.app.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}')
        self.app['bg'] = 'gray10'

        self.canvas = Canvas(self.app, width=WIN_WIDTH, height=WIN_HEIGHT, bg='gray10')
        self.canvas.pack()
        
        self.run(force_reload=True)
        self.app.mainloop()

    def print_data(self):
        font = 'white'
        self.canvas.create_text(
            WIN_WIDTH * 0.8,
            WIN_HEIGHT * 0.1,
            text='Turn: ' + str(self.game.data.turn),
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.8,
            WIN_HEIGHT * 0.15,
            text='Agent Amount: ' + str(self.game.data.agent_amount),
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.8,
            WIN_HEIGHT * 0.25,
            text='Player',
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.9,
            WIN_HEIGHT * 0.25,
            text='Opponent',
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.7,
            WIN_HEIGHT * 0.3,
            text='Stacked Agent:',
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.8,
            WIN_HEIGHT * 0.3,
            text=self.game.data.player_stack,
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.9,
            WIN_HEIGHT * 0.3,
            text=self.game.data.opponent_stack,
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.7,
            WIN_HEIGHT * 0.35,
            text='Area Point:',
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.8,
            WIN_HEIGHT * 0.35,
            text=self.game.data.player_area_points,
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.9,
            WIN_HEIGHT * 0.35,
            text=self.game.data.opponent_area_points,
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.7,
            WIN_HEIGHT * 0.4,
            text='Wall Point:',
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.8,
            WIN_HEIGHT * 0.4,
            text=self.game.data.player_wall_points,
            fill=font,
            font=('Purisa', 30)
        )
        self.canvas.create_text(
            WIN_WIDTH * 0.9,
            WIN_HEIGHT * 0.4,
            text=self.game.data.opponent_wall_points,
            fill=font,
            font=('Purisa', 30)
        )

        # Button(self.canvas, text='終了', command=sys.exit).pack()

    def run(self, force_reload=False):
        self.app.after(50, self.run)

        flag = force_reload
        if self.is_online:
            flag = get('http://localhost:5000/procon-progress').content.decode()
        else:
            flag = self.game.progress()

        if flag == 'True':
            flag = True
        else:
            flag = False

        if flag:
            self.canvas.delete('all')

            if self.is_online:
                self.game.data = Data.from_json(loads(get('http://localhost:5000/procon-data').content))

            cell_width  = WIN_WIDTH * 0.6 / self.game.data.board_size.x
            cell_height = (WIN_HEIGHT - 2 * WIN_MARGIN + CELL_MARGIN) / self.game.data.board_size.y
            for x in range(1, self.game.data.board_size.x + 1):
                for y in range(1, self.game.data.board_size.y + 1):
                    fill = AREA_COLORS[self.game.data.areas_board[Point(x, y)] + 1]
                    font = 'black'

                    if self.game.data.walls_board[Point(x, y)] != 0:
                        fill = WALL_COLORS[self.game.data.walls_board[Point(x, y)] + 1]
                        font = 'gray90'

                    if self.game.data.agents_board[Point(x, y)] != 0:
                        fill = AGENT_COLORS[self.game.data.agents_board[Point(x, y)] + 1]
                        font = 'gray90'

                    self.canvas.create_rectangle(
                        WIN_MARGIN + (x - 1) * cell_width,
                        WIN_MARGIN + (y - 1) * cell_height,
                        WIN_MARGIN + x * cell_width  - CELL_MARGIN,
                        WIN_MARGIN + y * cell_height - CELL_MARGIN,
                        fill=fill,
                        outline=''
                    )
                    self.canvas.create_text(
                        WIN_MARGIN + (x - 0.5) * cell_width  - CELL_MARGIN / 2,
                        WIN_MARGIN + (y - 0.5) * cell_height - CELL_MARGIN / 2,
                        text=str(self.game.data.points_board[Point(x, y)]),
                        fill=font,
                        font=('Purisa', 20)
                    )

                    self.print_data()