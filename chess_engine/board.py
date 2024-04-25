from utils.const import *
from chess_engine.piece import *
from chess_engine.move import Move
from chess_engine.square import Square

class Board:

    def __init__(self):
        self.squares = []
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        # Cập nhật bàn cờ sau nước đi
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Kiểm tra điều kiện nhập thành
        if piece.name == 'king':
            row = 0 if piece.color == 'black' else 7 
            diff = initial.col - final.col
            if diff == 2:
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    piece.moved = True
                    piece.moves = []
                    # Di chuyển xe trái
                    piece2 = self.squares[row][0].piece
                    initial = Square(row, 0)
                    final = Square(row, 3)
                    move2 = Move(initial, final)
                    self.move(piece2, move2)
            elif diff == -2:
                piece.moved = True
                piece.moves = []
                # Di chuyển xe phải
                piece2 = self.squares[row][7].piece
                initial = Square(row, 7)
                final = Square(row, 5)
                move2 = Move(initial, final)
                self.move(piece2, move2)

        # Kiểm tra điều kiện phong tốt
        if piece.name == 'pawn':
            self.check_promotion(piece, final)

        piece.moved = True
        piece.moves = []

        self.last_move = move

    def check_promotion(self, piece, final):
        promote_row = 0 if piece.color == 'white' else 7

        if final.row == promote_row:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def check_mate(self):
        white_king = False
        black_king = False

        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    if piece.color == 'white':
                        if piece.name == 'king':
                            white_king = True
                    else:
                        if piece.name == 'king':
                            black_king = True

        if white_king and black_king: return 0
        if white_king: return 1
        if black_king: return -1

    def check_stale_mate(self):
        count_moves_white = 0
        count_moves_black = 0

        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    self.calc_moves(piece, row, col)
                    if piece.color == 'white':
                        count_moves_white += len(piece.moves)
                    else:
                        count_moves_black += len(piece.moves)

        # if count_moves_white != 0 and count_moves_black != 0:
        #     0
        # return 1
        print('count_moves_white:', count_moves_white)
        print('count_moves_black:', count_moves_black)
        if count_moves_white == 0 or count_moves_black == 0:
            return 1
        return 0


    def valid_move(self, piece, move):
        return move in piece.moves

    # Tính toán các nước đi có thể của quân cờ
    def calc_moves(self, piece, row, col):
        def pawn():
            piece = self.squares[row][col].piece
            if piece.color == 'black':
                if row != 1: piece.moved = True
            if piece.color == 'white':
                if row != 6: piece.moved = True
            # Quân tốt có thể đi thẳng 1 hoặc 2 ô nếu chưa di chuyển
            steps = 1 if piece.moved else 2

            # Kiểm tra ô phía trước
            start = row + piece.dir
            end = row + piece.dir * (1 + steps)
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, col, self.squares[move_row][col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break
            
            # Kiểm tra 2 ô chéo phía trước
            move_cols = [col - 1, col + 1]
            move_row = row + piece.dir
            for move_col in move_cols:
                if Square.in_range(move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def knight():
            # Các nước đi có thể của quân mã
            possible_moves = [
            (row - 2, col + 1),
            (row - 1, col + 2),
            (row + 1, col + 2),
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row + 1, col - 2),
            (row - 1, col - 2),
            (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                move_row, move_col = possible_move
                if Square.in_range(move_row, move_col):
                    # Nếu ô đó trống hoặc có quân đối phương
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)

        # Kiêm tra các nước đi có thể của quân cờ di chuyển theo các đường thẳng
        def straightline(incrs):
            for incr in incrs:
                row_inc, col_inc = incr
                move_row = row + row_inc
                move_col = col + col_inc
                while True:
                    if Square.in_range(move_row, move_col):
                        # Ô trống hoặc có quân đối phương
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        # Ô trống
                        if self.squares[move_row][move_col].isempty():
                            piece.add_move(move)
                        # Có quân đối phương
                        else: 
                            if self.squares[move_row][move_col].has_rival_piece(piece.color):
                                piece.add_move(move)
                            break
                    else: # not in range
                        break
                
                    # incr
                    move_row, move_col = move_row + row_inc, move_col + col_inc

        def king():
            adjs = [
                (row - 1, col + 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1),
            ]

            # Kiểm tra các ô xung quanh
            for adj in adjs:
                move_row, move_col = adj
                
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        if not self.is_square_under_attack(move_row, move_col, piece.color):
                            piece.add_move(move)
                
            # Kiểm tra điều kiện nhập thành
            if not piece.moved and not self.is_square_under_attack(row, col, piece.color):
                # Nhập thành bên trái
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    if not lRook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): break
                            if c == 3:
                                # new move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                if not self.is_square_under_attack(row, 2, piece.color):
                                    move = Move(initial, final)
                                    piece.add_move(move)

                # Nhâp thành bên phải
                rRook = self.squares[row][7].piece
                if isinstance(rRook, Rook):
                    if not rRook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): break
                            if c == 6:
                                # new move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                if not self.is_square_under_attack(row, 6, piece.color):
                                    move = Move(initial, final)
                                    piece.add_move(move)

        if piece.name == 'pawn': 
            pawn()

        elif piece.name == 'knight': 
            knight()

        elif piece.name == 'bishop': 
            straightline([(-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'rook': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1)])

        elif piece.name == 'queen': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'king': 
            king()

    def is_square_under_attack(self, move_row, move_col, color):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.piece is not None and square.piece.color != color:
                    # self.calc_moves(square.piece, row, col)
                    # for move in square.piece.moves:
                    #     if move.final.row == move_row and move.final.col == move_col:
                    #         return True
                    # if self.can_attack(square.piece, row, col, move_row, move_col):
                    #     print('piece:', square.piece.name)
                    #     print('row:', row, 'col:', col)
                    #     print('can_attack:', self.can_attack(square.piece, row, col, move_row, move_col))
                    if self.can_attack(row, col, move_row, move_col):
                        return True
        return False
    
    def can_attack(self, row, col, move_row, move_col):
        piece = self.squares[row][col].piece
        def pawn():
            if piece.color == 'black':
                dir = 1
            else:
                dir = -1

            if move_row == row + dir and (move_col == col - 1 or move_col == col + 1):
                return True

        def knight():
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                if possible_move == (move_row, move_col):
                    return True

        def bishop():
            if abs(move_row - row) == abs(move_col - col):
                return self.is_path_clear(row, col, move_row, move_col)

        def rook():
            if move_row == row or move_col == col:
                return self.is_path_clear(row, col, move_row, move_col)

        def queen():
            # if abs(move_row - row) == abs(move_col - col) or move_row == row or move_col == col:
            #     return self.is_path_clear(row, col, move_row, move_col)
            return bishop() or rook()

        def king():
            if abs(move_row - row) <= 1 and abs(move_col - col) <= 1:
                return True

        if piece.name == 'pawn': return pawn()
        if piece.name == 'knight': return knight()
        if piece.name == 'bishop': return bishop()
        if piece.name == 'rook': return rook()
        if piece.name == 'queen': return queen()
        if piece.name == 'king': return king()


    def is_path_clear(self, start_row, start_col, end_row, end_col):
        row_step = 0 if start_row == end_row else 1 if start_row < end_row else -1
        col_step = 0 if start_col == end_col else 1 if start_col < end_col else -1

        row, col = start_row + row_step, start_col + col_step
        while row != end_row or col != end_col:
            if self.squares[row][col].has_piece():
                return False
            row += row_step
            col += col_step

        return True

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # Quân tốt
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Quân mã
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Quân tượng
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Quân xe
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Quân hậu
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # Quân vua
        self.squares[row_other][4] = Square(row_other, 4, King(color))