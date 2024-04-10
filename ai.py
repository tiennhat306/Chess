import copy, math, random

from utils.const import *

class AI:

    def __init__(self, depth=3):
        self.depth = depth
        self.color = 'black'
        self.game_moves = []
        self.explored = 0

    # -------
    # MINIMAX - ALPHA BETA
    # -------

    def scoremap(self, piece, row, col):
        scores = 0
        if piece.name == 'pawn':
            pawn_scores = [
                [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
            ]
            if piece.color == 'white':
                scores = pawn_scores

            elif piece.color == 'black':
                scores = pawn_scores[::-1]

        elif piece.name == 'knight':
            knight_scores = [
                [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]
            ]
            if piece.color == 'white':
                scores = knight_scores
            elif piece.color == 'black':
                scores = knight_scores[::-1]

        elif piece.name == 'bishop':
            bishop_scores = [
                [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]
            ]
            if piece.color == 'white':
                scores = bishop_scores
            elif piece.color == 'black':
                scores = bishop_scores[::-1]

        elif piece.name == 'rook':
            rook_scores = [
                [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]
            ]
            if piece.color == 'white':
                scores = rook_scores
            elif piece.color == 'black':
                scores = rook_scores[::-1]

        elif piece.name == 'queen':
            queen_scores = [
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]
            ]
            if piece.color == 'white':
                scores = queen_scores
            elif piece.color == 'black':
                scores = queen_scores[::-1]
        
        # elif piece.name == 'king':
        #     king_scores = [
        #         [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        #         [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        #         [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        #         [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        #         [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        #         [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        #         [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
        #         [0.05, 0.50, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05]
        #     ]
        #     if piece.color == 'white':
        #         scores = king_scores
        #
        #     elif piece.color == 'black':
        #         scores = king_scores[::-1]


        # eval = -scores[row][col] if piece.color == 'black' else scores[row][col]
        return scores[row][col]

    # def threats(self, board, piece):
    #     eval = 0
    #     for move in piece.moves:
    #         attacked = board.squares[move.final.row][move.final.col]
    #         if attacked.has_piece():
    #             if attacked.piece.color != piece.color:
    #                 # checks
    #                 if attacked.piece.name == 'king':
    #                     eval += attacked.piece.value / 10500
    #
    #                 # threat
    #                 else:
    #                     eval += attacked.piece.value / 45
    #
    #     return eval

    def score_board(self, board):
        # var
        score = 0

        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    # piece
                    piece =  board.squares[row][col].piece

                    piece_position_score = 0
                    if piece.name != 'king':
                        piece_position_score = self.scoremap(piece, row, col)
                    if piece.color == 'white':
                        score -= piece.value + piece_position_score
                    elif piece.color == 'black':
                        score += piece.value + piece_position_score

                    # score += piece.value
                    # # scoremap
                    # score += self.scoremap(piece, row, col)
                    # # moves
                    # if piece.name != 'queen':
                    #     score += 0.01 * len(piece.moves)
                    # else:
                    #     score += 0.003 * len(piece.moves)
                    # # checks
                    # score += self.threats(board, piece)

        # score = round(score, 5)
        return score

    def get_moves(self, board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_team_piece(color):
                    board.calc_moves(square.piece, square.row, square.col)
                    moves += square.piece.moves
        
        return moves

    def minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0:
            return self.score_board(board), None # eval, move
        
        # white
        if maximizing:
            max_eval = -math.inf
            moves = self.get_moves(board, 'black')
            for move in moves:
                self.explored += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth-1, False, alpha, beta)[0] # eval, mov
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, max_eval)
                if beta <= alpha: break

            if not best_move:
                best_move = moves[0]

            return max_eval, best_move # eval, move
        
        # black
        elif not maximizing:
            min_eval = math.inf
            moves = self.get_moves(board, 'white')
            for move in moves:
                self.explored += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth-1, True, alpha, beta)[0] # eval, move
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, min_eval)
                if beta <= alpha: break
            
            if not best_move:
                idx = random.randrange(0, len(moves))
                best_move = moves[idx]

            return min_eval, best_move # eval, move


    def find_best_move(self, main_board):
        self.explored = 0

        # add last move
        last_move = main_board.last_move
        self.game_moves.append(last_move)

        print('\nFinding best move...')

        # minimax initial call
        eval, move = self.minimax(main_board, self.depth, True, -math.inf, math.inf) # eval, move

        # printing
        print('\n- Initial eval:', self.score_board(main_board))
        print('- Final eval:', eval)
        print('- Boards explored', self.explored)
        # if eval >= 5000: print('* White MATE!')
        # if eval <= -5000: print('* Black MATE!')
            
        # append
        self.game_moves.append(move)
        
        return move