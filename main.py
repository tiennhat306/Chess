import sys, pygame

from utils.const import *
from views.game import Game
from chess_engine.move import Move
from chess_engine.square import Square

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        ai = self.game.ai
        dragger = self.game.dragger

        while True:
            
            if not game.selected_piece:
                game.show_bg(screen)
                game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                
                # mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    pos = event.pos
                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_col = dragger.mouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece ?
                        if piece.color == game.next_player:
                            game.select_piece(piece)
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.drag_piece(piece)
                            dragger.save_initial(pos)
                            # show
                            game.show_bg(screen)
                            game.show_pieces(screen)

                # mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # released pos
                        released_row = dragger.mouseY // SQUARE_SIZE
                        released_col = dragger.mouseX // SQUARE_SIZE

                        # new move object
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        # valid move -> move ?
                        if board.valid_move(dragger.piece, move):
                            # capture
                            captured = board.squares[released_row][released_col].has_piece()
                            # move
                            board.move(dragger.piece, move)
                            game.sound_effect(captured)
                            # draw
                            game.show_bg(screen)
                            game.show_pieces(screen)
                            # next -> AI
                            game.next_turn()
                            
                            # --------------
                            # >>>>> AI >>>>>
                            # --------------

                            # update
                            game.unselect_piece()
                            game.show_pieces(screen)
                            pygame.display.update()
                            # optimal move
                            move = ai.eval(board)
                            initial = move.initial
                            final = move.final
                            # piece
                            piece = board.squares[initial.row][initial.col].piece
                            # capture
                            captured = board.squares[final.row][final.col].has_piece()
                            # move
                            board.move(piece, move)
                            game.sound_effect(captured)
                            # draw
                            game.show_bg(screen)
                            game.show_pieces(screen)
                            # next -> AI
                            game.next_turn()
                    
                    game.unselect_piece()
                    dragger.undrag_piece()

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    motion_row = pos[1] // SQUARE_SIZE
                    motion_col = pos[0] // SQUARE_SIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show
                        game.show_bg(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # key press
                elif event.type == pygame.KEYDOWN:

                    
                    # reset
                    if event.key == pygame.K_r:
                        game.reset()

                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        ai = self.game.ai
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    
if __name__ == '__main__':
    m = Main()
    m.mainloop()