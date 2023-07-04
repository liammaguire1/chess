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

# Font
FONT = pygame.font.SysFont('timesnewroman', 40)

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

        # Set key-value pairs to (i, j): Square
        sq_ob.piece = p_obj
        squares[square] = sq_ob
    
    # Persistent variables
    running = True
    white = True
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
                
                # Click on piece
                for sq in squares:
                    if squares[sq].piece:
                        if white and squares[sq].piece.color == 'white' or not white and squares[sq].piece.color == 'black':
                            mouse_pos = pygame.mouse.get_pos()
                            if squares[sq].piece.rect.collidepoint(mouse_pos):
                                current_piece = squares[sq].piece
                                current_square = sq

            # User released mouse button
            if event.type == pygame.MOUSEBUTTONUP:
                if current_piece:
                    squares, white, new_square = lock_piece(squares, current_piece, current_square, white, captured_pieces)

                    # Add valid move to list of played moves
                    if current_square != new_square:
                        move = (current_piece, current_square, new_square)
                        played_moves.append(move)
                current_piece = None
        
        # Moving pieces
        if current_piece:
            drag_piece(current_piece)
            
        # Draw on window
        draw_window(squares, PIECE_IMGS, white, played_moves, captured_pieces)       

    pygame.quit()


def draw_window(squares, images, white, played_moves, captured_pieces):

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
                highlight_rect = pygame.Rect((7 - sq[1]) * SQUARE_SIDE, (7 - sq[0]) * SQUARE_SIDE + SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE)
                pygame.draw.rect(WINDOW, ORANGE, highlight_rect)

    # Draw pieces
    for sq in squares:
        if squares[sq].piece:
            WINDOW.blit(images[squares[sq].piece.name], (squares[sq].piece.rect.x, squares[sq].piece.rect.y))

    # Draw header text
    if white:
        turn_text = "White to move..."
        header_text = FONT.render(turn_text, 1, WHITE)
    else:
        turn_text = "Black to move..."
        header_text = FONT.render(turn_text, 1, BLACK)
    WINDOW.blit(header_text, (WIDTH * .25, 10))

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


def lock_piece(squares, piece, current_square, white, captured_pieces):
    mouse_pos = pygame.mouse.get_pos()
    for sq in squares:
        if squares[sq].rect.collidepoint(mouse_pos):

            # All possible moves
            moves = piece.moves(current_square, squares)
            print(moves)
            
            # Invalid: capture same color
            if squares[sq].piece:
                if squares[sq].piece.color == piece.color:
                    break

            # Invalid: not an available move
            if sq not in moves:
                break

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

            # Flip board and return
            squares = flip_board(squares)
            return squares, not white, sq
    
    # Reset piece after lock failed
    piece.rect.x = current_square[1] * SQUARE_SIDE
    piece.rect.y = current_square[0] * SQUARE_SIDE + SQUARE_SIDE 
    return squares, white, current_square


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

if __name__ == "__main__":
    main()