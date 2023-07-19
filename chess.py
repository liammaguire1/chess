import pygame
import os
import copy

from pieces import *
pygame.font.init()

# Set window dimensions & caption
WIDTH, HEIGHT = 512, 640
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Set square & piece dimensions
SQUARE_SIDE = WIDTH/8

# RGB color values
PINK = (234, 202, 252)
ALMOND = (234, 221, 202)
COFFEE = (111, 78, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (252, 196, 73)
YELLOW = (255, 255, 156)

# Font
FONT = pygame.font.SysFont('timesnewroman', 40, bold=True)
BUTTONFONT = pygame.font.SysFont('timesnewroman', 18)

def main():
    
    # Dict to store square data
    squares = {}

    # Load piece images into a dict
    PIECE_IMGS = {}
    for img in os.listdir('Assets'):
        piece_img = pygame.image.load(os.path.join('Assets', img))
        piece_img = pygame.transform.scale(piece_img, (SQUARE_SIDE, SQUARE_SIDE))
        name = img[:(len(img)-4)]
        PIECE_IMGS[name] = piece_img

    # Initialize 2D array of tuples to create board
    SQUARES = []
    for i in range(8):
        for j in range(8):
            square = (i, j)
            SQUARES.append(square)

    # Create objects
    for square in SQUARES:

        # Create Square object
        rect = pygame.Rect((square[1] * SQUARE_SIDE), (square[0] * SQUARE_SIDE + SQUARE_SIDE), SQUARE_SIDE, SQUARE_SIDE)
        sq_ob = Square(rect)
        
        # Initial placement of pieces
        if square in [(0,0), (0,7)]:
            piece = 'black-rook'
        elif square in [(0,1), (0,6)]:
            piece = 'black-knight'
        elif square in [(0,2), (0,5)]:
            piece = 'black-bishop'
        elif square == (0, 3):
            piece = 'black-queen'
        elif square == (0, 4):
            piece = 'black-king'
        elif square[0] == 1:
            piece = 'black-pawn'
        elif square in [(7,0), (7,7)]:
            piece = 'white-rook'
        elif square in [(7,1), (7,6)]:
            piece = 'white-knight'
        elif square in [(7,2), (7,5)]:
            piece = 'white-bishop'
        elif square == (7, 3):
            piece = 'white-queen'
        elif square == (7, 4):
            piece = 'white-king'
        elif square[0] == 6:
            piece = 'white-pawn'
        else:
            piece = None

        # Create Piece object
        if piece:
            p_rect = pygame.Rect(square[1] * SQUARE_SIDE, square[0] * SQUARE_SIDE + SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE)
            p_name = piece[6:].capitalize()
            color = 'white' if piece[0] == 'w' else 'black'
            p_obj = eval(f'{p_name}("{piece}", "{color}")')
            p_obj.rect = p_rect
        else:
            p_obj = None

        # Set key-value pairs to '(i, j): Square'
        sq_ob.piece = p_obj
        squares[square] = sq_ob

    # 'Draw' button
    draw = pygame.Rect(SQUARE_SIDE/4, SQUARE_SIDE/4, SQUARE_SIDE, SQUARE_SIDE/2)
    
    # Persistent variables
    running = True
    white = True
    game_over = 0
    play_again = None
    current_piece = None
    current_square = None
    played_moves = []
    captured_pieces = []
    
    # Main gameplay loop
    while running:
        
        # Check for events
        for event in pygame.event.get():
        
            # User closed window
            if event.type == pygame.QUIT:
                running = False

            # User clicked mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                mouse_pos = pygame.mouse.get_pos()
                
                # 'Draw' button
                if draw.collidepoint(mouse_pos) and game_over == 0:
                    game_over = 2

                # 'Play again' button
                if play_again:
                    if play_again.collidepoint(mouse_pos):
                        main()
                
                # Click on piece
                if not game_over:
                    for sq in squares:
                        if squares[sq].piece:
                            if white and squares[sq].piece.color == 'white' or not white and squares[sq].piece.color == 'black':
                                if squares[sq].piece.rect.collidepoint(mouse_pos):
                                    current_piece = squares[sq].piece
                                    current_square = sq

            # User released mouse button
            if event.type == pygame.MOUSEBUTTONUP:
                if current_piece:
                    squares, white, new_square, game_over = lock_piece(squares, current_piece, current_square, white, captured_pieces, played_moves)

                    # Add valid move to list of played moves
                    if current_square != new_square:
                        move = (current_piece, current_square, new_square)
                        played_moves.append(move)
                current_piece = None
        
        # Move pieces
        if current_piece:
            drag_piece(current_piece)

        # 'Play again' button
        if game_over > 0:
            play_again = pygame.Rect(SQUARE_SIDE * 6, SQUARE_SIDE/4, SQUARE_SIDE * 1.5, SQUARE_SIDE/2)

        # Draw on window
        draw_window(squares, PIECE_IMGS, white, played_moves, captured_pieces, game_over, draw, play_again)       

    pygame.quit()


def draw_window(squares, images, white, played_moves, captured_pieces, game_over, draw, play_again):

    # Set background color
    WINDOW.fill(PINK)
    
    # Draw squares
    for sq in squares:
        if (sq[0] + sq[1]) % 2 == 0:
            pygame.draw.rect(WINDOW, ALMOND, squares[sq].rect)
        else:
            pygame.draw.rect(WINDOW, COFFEE, squares[sq].rect)

    # Highlight squares
    for sq in squares:
        if played_moves:
            if sq == played_moves[-1][1] or sq == played_moves[-1][2]:
                if game_over in [1, 3]:
                    highlight_rect = pygame.Rect((sq[1]) * SQUARE_SIDE, (sq[0]) * SQUARE_SIDE + SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE)
                else:
                    highlight_rect = pygame.Rect((7 - sq[1]) * SQUARE_SIDE, (7 - sq[0]) * SQUARE_SIDE + SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE)
                pygame.draw.rect(WINDOW, ORANGE, highlight_rect)

    # Draw pieces
    for sq in squares:
        if squares[sq].piece:
            WINDOW.blit(images[squares[sq].piece.name], (squares[sq].piece.rect.x, squares[sq].piece.rect.y))

    # Draw header text
    player = 'White' if white else 'Black'
    if game_over == 3:
        turn_text = "  Stalemate!"
    elif game_over == 2:
        turn_text = "It's a draw!"
    elif game_over == 1:
        turn_text = f"{player} wins!"
    else:
        turn_text = f"{player} to move..."
    header_text = FONT.render(turn_text, 1, eval(player.upper()))
    WINDOW.blit(header_text, (WIDTH * .25, 10))

    # Draw 'Draw' button
    draw_text = BUTTONFONT.render("Draw?", 1, BLACK)
    pygame.draw.rect(WINDOW, YELLOW, draw, border_radius=8)
    pygame.draw.rect(WINDOW, BLACK, draw, width=1, border_radius=8)
    WINDOW.blit(draw_text, (draw.x + 8, draw.y + 4))

    # Draw 'Play again' button
    if play_again:
        play_again_text = BUTTONFONT.render("Play Again?", 1, BLACK)
        pygame.draw.rect(WINDOW, YELLOW, play_again, border_radius=8)
        pygame.draw.rect(WINDOW, BLACK, play_again, width=1, border_radius=8)
        WINDOW.blit(play_again_text, (play_again.x + 5, play_again.y + 4))

    # Draw captured pieces
    drawn_pieces = []
    for piece in captured_pieces:
        if piece.color == 'white':
            if type(piece) == Pawn:
                cap_rect = pygame.Rect(0, SQUARE_SIDE * 9, SQUARE_SIDE/2, SQUARE_SIDE/2)
            else:
                cap_rect = pygame.Rect(0, SQUARE_SIDE * 9.5, SQUARE_SIDE/2, SQUARE_SIDE/2)
        else:
            if type(piece) == Pawn:
                cap_rect = pygame.Rect(SQUARE_SIDE * 4, SQUARE_SIDE * 9, SQUARE_SIDE/2, SQUARE_SIDE/2)
            else:
                cap_rect = pygame.Rect(SQUARE_SIDE * 4, SQUARE_SIDE * 9.5, SQUARE_SIDE/2, SQUARE_SIDE/2)
        
        while cap_rect.collidelist(drawn_pieces) != -1:
            cap_rect.x += SQUARE_SIDE/2
        
        drawn_pieces.append(cap_rect)
        small_piece = pygame.transform.scale(images[piece.name], (SQUARE_SIDE/2, SQUARE_SIDE/2))
        WINDOW.blit(small_piece, (cap_rect.x, cap_rect.y))

    pygame.display.update()


def drag_piece(piece):
    mouse_pos = pygame.mouse.get_pos()
    piece.rect.x = mouse_pos[0] - SQUARE_SIDE/2
    piece.rect.y = mouse_pos[1] - SQUARE_SIDE/2


def lock_piece(squares, piece, current_square, white, captured_pieces, played_moves):
    mouse_pos = pygame.mouse.get_pos()
    for sq in squares:
        if squares[sq].rect.collidepoint(mouse_pos):

            # All possible moves
            if type(piece) == Pawn:
                moves = piece.moves(current_square, squares, played_moves)
            else:
                moves = piece.moves(current_square, squares)
            #print(moves)
            
            # Invalid: capture same color
            if squares[sq].piece:
                if squares[sq].piece.color == piece.color:
                    break

            # Invalid: not an available move
            if sq not in moves:
                break

            # Invalid: in check
            if check(squares, current_square, sq, piece, white, played_moves):
                break

            # Castle
            if type(piece) == King and abs(sq[1] - current_square[1]) == 2:
                pass

            # En passant capture
            if type(piece) == Pawn and sq[1] != current_square[1] and not squares[sq].piece:
                captured_pieces.append(squares[(sq[0] + 1, sq[1])].piece)
                squares[(sq[0] + 1, sq[1])].piece = None

            # Capture a piece
            if squares[sq].piece:
                captured_pieces.append(squares[sq].piece)
                                    
            # Update Square data after lock succeeded
            squares[current_square].piece = None
            squares[sq].piece = piece

            # Update 'moved' status for piece
            piece.moved = True
            
            # Update visual representation of piece
            piece.rect.x = squares[sq].rect.x
            piece.rect.y = squares[sq].rect.y

            # Test for checkmate
            sq_copy = flip_board(copy.deepcopy(squares))            
            if check(sq_copy, (7 - current_square[0], 7 - current_square[1]), (7 - sq[0], 7 - sq[1]), piece, not white, played_moves):
                if mate(sq_copy, not white, played_moves):
                    return squares, white, sq, 1
            # Test for stalemate
            else:
                if mate(sq_copy, not white, played_moves):
                    return squares, white, sq, 3
            
            # Flip board and return
            squares = flip_board(squares)
            return squares, not white, sq, 0
    
    # Reset piece after lock failed
    piece.rect.x = current_square[1] * SQUARE_SIDE
    piece.rect.y = current_square[0] * SQUARE_SIDE + SQUARE_SIDE 
    return squares, white, current_square, 0


def flip_board(squares):
    s_new = {}
    for sq in squares:
        s_new[sq] = squares[(7 - sq[0], 7 - sq[1])]
        s_new[sq].rect.x = 448 - squares[(7 - sq[0], 7 - sq[1])].rect.x
        s_new[sq].rect.y = 576 - squares[(7 - sq[0], 7 - sq[1])].rect.y
        
        if s_new[sq].piece:
            s_new[sq].piece.rect.x = 448 - squares[(7 - sq[0], 7 - sq[1])].piece.rect.x
            s_new[sq].piece.rect.y = 576 - squares[(7 - sq[0], 7 - sq[1])].piece.rect.y
    return s_new


def check(squares, current_sq, new_sq, piece, white, played_moves):
    
    # Player to be checked
    color = 'white' if white else 'black'
    
    # Copy board
    squares = copy.deepcopy(squares)

    # Try move
    squares[current_sq].piece = None
    squares[new_sq].piece = piece

    # Locate king
    for sq in squares:
        if squares[sq].piece:
            if type(squares[sq].piece) == King and squares[sq].piece.color == color:
                king = (7 - sq[0], 7 - sq[1])

    # Flip board
    squares = flip_board(copy.deepcopy(squares))

    # Test if opposing pieces see king
    for sq in squares:
        if squares[sq].piece:
            if white and squares[sq].piece.color == 'black' or not white and squares[sq].piece.color == 'white':
                
                # Vision of pieces
                if type(squares[sq].piece) == Pawn:
                    vision = squares[sq].piece.moves(sq, squares, played_moves)
                else:
                    vision = squares[sq].piece.moves(sq, squares)

                # King in vision
                if king in vision:
                    return True
    return False


def mate(squares, white, played_moves):
    
    for sq in squares:
        if squares[sq].piece:
            if white and squares[sq].piece.color == 'white' or not white and squares[sq].piece.color == 'black':
                
                # Available moves for piece
                if type(squares[sq].piece) == Pawn:
                    moves = squares[sq].piece.moves(sq, squares, played_moves)
                else:
                    moves = squares[sq].piece.moves(sq, squares)
                
                # Test if move removes check
                for move in moves:
                    if not check(squares, sq, move, squares[sq].piece, white, played_moves):
                        return False
    return True


if __name__ == "__main__":
    main()