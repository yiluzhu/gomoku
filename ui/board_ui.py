import tkinter as tk
from tkinter import messagebox

from utils import index_to_pixel, pixels_to_indices
from constants import BOARD_WIDTH_PIXELS, BOARD_SIZE, PIECE_RADIUS_PIXELS, VersusMode, CENTER_POINT


class GameBoardUI(tk.Canvas):
    def __init__(self, master, model, height, width):
        super().__init__(master, height=height, width=width)
        self.pack()
        self.game_model = model
        self.master.master.config(menu=self.get_menu_bar())
        self.versus_mode = None
        self.bind('<Button-1>', self.on_click)

    def draw_board_canvas(self):
        """Initialize game board"""
        for i in range(BOARD_SIZE):
            # draw vertical lines
            self.create_line(index_to_pixel(i),
                             index_to_pixel(0),
                             index_to_pixel(i),
                             index_to_pixel(BOARD_SIZE - 1))
            # draw horizontal lines
            self.create_line(index_to_pixel(0),
                             index_to_pixel(i),
                             index_to_pixel(BOARD_SIZE - 1),
                             index_to_pixel(i))

    def on_click(self, event):
        """Listen to mouse event, decide piece position on board based on mouse pixel values"""
        if not self.versus_mode:
            messagebox.showinfo('ERROR', 'Please start a game from the menu.')
            return

        point_indices = pixels_to_indices(event.x, event.y)
        if not point_indices:
            return

        x, y = point_indices
        player_data = self.game_model.on_click(x, y)
        can_continue = self.process_game_data(player_data)
        if can_continue and self.versus_mode != VersusMode.PvP:
            ai_data = self.game_model.ai_move()
            self.process_game_data(ai_data)

    def process_game_data(self, data):
        """Given data returned from game model, draw pieces accordingly"""
        piece_color = data.get('piece_color')
        if piece_color:
            x = data.get('x')
            y = data.get('y')
            self.create_oval(index_to_pixel(x) - PIECE_RADIUS_PIXELS,
                             index_to_pixel(y) - PIECE_RADIUS_PIXELS,
                             index_to_pixel(x) + PIECE_RADIUS_PIXELS,
                             index_to_pixel(y) + PIECE_RADIUS_PIXELS,
                             fill=piece_color)
        else:
            return False

        if data.get('win'):
            text = '{} wins'.format(piece_color).upper()
            self.create_text(BOARD_WIDTH_PIXELS / 2, BOARD_WIDTH_PIXELS, text=text)
            self.unbind('<Button-1>')
            return False
        else:
            return True

    def get_menu_bar(self):
        menu_bar = tk.Menu(self)
        versus_mode_menu = tk.Menu(menu_bar)
        versus_mode_menu.add_command(label='Player(black) vs Player(white)', command=lambda: self.start_game(VersusMode.PvP))
        versus_mode_menu.add_command(label='Player(black) vs AI(white)', command=lambda: self.start_game(VersusMode.PvA))
        versus_mode_menu.add_command(label='AI(black) vs Player(white)', command=lambda: self.start_game(VersusMode.AvP))
        menu_bar.add_cascade(label='Start', menu=versus_mode_menu)
        return menu_bar

    def reset(self):
        self.delete('all')
        self.versus_mode = None
        self.bind('<Button-1>', self.on_click)

    def start_game(self, mode):
        """Set versus mode"""
        if self.versus_mode:
            self.reset()
            self.game_model.reset()

        self.versus_mode = mode
        self.game_model.set_versus_mode(mode)
        self.draw_board_canvas()
        if mode == VersusMode.AvP:
            ai_data = self.game_model.ai_move(*CENTER_POINT)
            self.process_game_data(ai_data)
