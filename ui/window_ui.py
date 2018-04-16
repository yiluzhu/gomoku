import tkinter as tk

from models.game import GameModel
from ui.board_ui import GameBoardUI
from constants import BOARD_HEIGHT_PIXELS, BOARD_WIDTH_PIXELS, VERSION


class GameApp(tk.Frame):
    """The app"""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title('Super AI Gomoku (version {})'.format(VERSION))
        self.model = GameModel()
        self.board_ui = GameBoardUI(self, self.model, height=BOARD_HEIGHT_PIXELS, width=BOARD_WIDTH_PIXELS)
