import pygame

from ai import AI
from utils.const import *
from chess_engine.board import Board
from views.config import Config
from chess_engine.square import Square
from views.dragger import Dragger

class Game:

    def __init__(self):
        self.board = Board()
        self.config = Config()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.selected_piece = None
        self.hovered_square = None
        self.result = -1

        self.ai = AI()

    def set_result(self, result):
        self.result = result

    def draw_end_game_text(self, surface):
        text = 'DRAW!' if self.result == 0 else 'BLACK WINS!' if self.result == 1 else 'WHITE WINS!' if self.result == 2 else ''
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # RGBA

        # Create the text surface
        font = pygame.font.Font(None, 36)

        text_surface = font.render(text, True, (255, 255, 255))

        # Calculate the position to center the text
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        # Draw the overlay and the text
        surface.blit(overlay, (0, 0))
        surface.blit(text_surface, text_rect)




    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light

                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    surface.blit(lbl, (5, 5 + row * SQUARE_SIZE))

                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light

                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    surface.blit(lbl, (col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 20))
        
        if self.board.last_move:
            self.show_last_move(surface)

        if self.selected_piece:
            self.show_moves(surface)

        if self.result != -1:
            self.draw_end_game_text(surface)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.selected_piece:
                        piece.set_texture()
                        texture = piece.texture
                        img = pygame.image.load(texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.selected_piece:
            theme = self.config.theme

            for move in self.selected_piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            theme = self.config.theme

            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.col + pos.row) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (self.hovered_square.col * SQUARE_SIZE, self.hovered_square.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect, 3)

    def sound_effect(self, captured):
        if captured: self.config.capture_sound.play()
        else: self.config.move_sound.play()

    def next_turn(self):
        self.next_player = 'black' if self.next_player == 'white' else 'white'

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def select_piece(self, piece):
        self.selected_piece = piece
    
    def unselect_piece(self):
        self.selected_piece = None

    def change_theme(self):
        self.config.change_theme()

    def reset(self):
        self.__init__()
