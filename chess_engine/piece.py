import os

class Piece:
    def __init__(self, name, color, value, texture_rect=None):
        # value_sign = 1 if color == 'white' else -1
        self.name = name
        self.color = color
        # self.value = value * value_sign
        self.value = value
        self.moved = False
        self.moves = []
        self.set_texture()
        self.texture_rect = texture_rect

    def __str__(self):
        return self.color[0] + self.name[0].upper() + self.name[1].upper()

    def add_move(self, move):
        self.moves.append(move)

    def set_texture(self, dragging=False):
        self.texture = os.path.join(
            f'static/images/imgs-{'dragging' if dragging else 'normal'}/{self.color}_{self.name}.png')


class Pawn(Piece): # Quân Tốt
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)

class Knight(Piece): # Quân Mã
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece): # Quân Tượng
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)

class Rook(Piece): # Quân Xe
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece): # Quân Hậu
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece): # Quân Vua
    def __init__(self, color):
        super().__init__('king', color, 10000.0)