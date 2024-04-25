import sys, pygame

from utils.const import *
from views.game import Game
from chess_engine.move import Move
from chess_engine.square import Square

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Cờ vua')
        self.game = Game()

    def loop(self):
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
                    # checkmate = self.check_mate()
                    # if checkmate == -1:
                    #     # game.draw_end_game_text(screen, 1)
                    #     game.set_result(1)
                    #     game.show_bg(screen)
                    #     game.show_pieces(screen)
                    #     # pygame.display.update()
                    #     # is_running = False
                    # elif checkmate == 1:
                    #     # game.draw_end_game_text(screen, 'TRẮNG THẮNG!')
                    #     game.set_result(2)
                    #     game.show_bg(screen)
                    #     game.show_pieces(screen)
                    #     # pygame.display.update()
                    #     # is_running = False

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

                        # released position
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

                            checkmate = self.check_mate()
                            if checkmate == -1:
                                game.set_result(1)
                                game.show_bg(screen)
                                game.show_pieces(screen)
                            elif checkmate == 1:
                                game.set_result(2)
                                game.show_bg(screen)
                                game.show_pieces(screen)
                            else:
                                # check_stalemate = board.check_stale_mate()
                                # if check_stalemate == 1:
                                #     game.set_result(0)
                                #     game.show_bg(screen)
                                #     game.show_pieces(screen)
                                #     # pygame.display.update()
                                #     # is_running = False
                                # else:

                                # Đến lượt -> AI
                                game.next_turn()

                                # --------- AI ----------

                                if game.gamemode == 'ai':
                                    # update
                                    game.unselect_piece()
                                    game.show_pieces(screen)
                                    pygame.display.update()
                                    # optimal move
                                    eval, move = ai.find_best_move(board)

                                    if move is not None :
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

                                        black_checkmate = self.check_mate()
                                        if black_checkmate == -1:
                                            game.set_result(1)
                                            game.show_bg(screen)
                                            game.show_pieces(screen)
                                        elif black_checkmate == 1:
                                            game.set_result(2)
                                            game.show_bg(screen)
                                            game.show_pieces(screen)
                                        else:
                                            # check_stalemate = board.check_stale_mate()
                                            # if check_stalemate == 1:
                                            #     game.set_result(0)
                                            #     game.show_bg(screen)
                                            #     game.show_pieces(screen)
                                            #     # pygame.display.update()
                                            #     # is_running = False
                                            # else:
                                            #     # next -> AI
                                            game.next_turn()
                                    
                                    elif move is None:
                                        if eval == 0:
                                            game.set_result(0)
                                            game.show_bg(screen)
                                            game.show_pieces(screen)
                                        else:
                                            game.set_result(2)
                                            game.show_bg(screen)
                                            game.show_pieces(screen)
                    
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
                    # gamemode
                    if event.key == pygame.K_a:
                        game.change_gamemode()

                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # press 1
                    if event.key == pygame.K_1:
                        game.board.change_promotion_piece('queen')
                    
                    # press 2
                    if event.key == pygame.K_2:
                        game.board.change_promotion_piece('rook')

                    # press 3
                    if event.key == pygame.K_3:
                        game.board.change_promotion_piece('bishop')

                    # press 4
                    if event.key == pygame.K_4:
                        game.board.change_promotion_piece('knight')

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

    def check_mate(self):
        check_mate = self.game.board.check_mate()
        print(f'* CHECK MATE: {check_mate}')
        if check_mate == -1:
            # print(f'* ĐEN THẮNG!')
            return -1;

        elif check_mate == 1:
            # print(f'* TRẮNG THẮNG!')
            return 1;



if __name__ == '__main__':
    m = Main()
    m.loop()