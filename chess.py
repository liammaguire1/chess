import pygame
import os

from pieces import *
pygame.font.init()

# Set window dimensions & caption
WIDTH, HEIGHT = 512, 640
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Set square & piece dimensions
SQUARE_SIDE = WIDTH/8
PIECE_SIZE = SQUARE_SIDE

# RGB color values
PINK = (234, 202, 252)
ALMOND = (234, 221, 202)
COFFEE = (111, 78, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
FONT = pygame.font.SysFont('timesnewroman', 40)

def main():
    
    # List of dicts to store complete square data
    squares = []

    # Load piece images into a dict
    PIECE_IMGS = {}
    for img in os.listdir('Assets'):
        piece_img = pygame.image.load(os.path.join('Assets', img))
        piece_img = pygame.transform.scale(piece_img, (PIECE_SIZE, PIECE_SIZE))
        name = img[:(len(img)-4)]
        PIECE_IMGS[name] = piece_img

    # Initialize 2D array of tuples to create board
    SQUARES = []
    for i in range(8):
        row = []
        for j in range(8):
            square = (i, j)
            row.append(square)
        SQUARES.append(row)

    # Create objects
    for row in SQUARES:
        for square in row:

            # Create Square object
            location = square
            rect = pygame.Rect((square[1] * SQUARE_SIDE), (square[0] * SQUARE_SIDE + SQUARE_SIDE), SQUARE_SIDE, SQUARE_SIDE)
            sq_ob = Square(location, rect)
            
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
                p_rect = pygame.Rect(sq_ob.location[1] * SQUARE_SIDE, sq_ob.location[0] * SQUARE_SIDE + SQUARE_SIDE, PIECE_SIZE, PIECE_SIZE)
                p_name = piece[6:].capitalize()
                color = 'white' if piece[0] == 'w' else 'black'
                p_obj = eval(f'{p_name}("{piece}", "{color}")')
                p_obj.rect = p_rect
            else:
                p_obj = None

            # Append Square object
            sq_ob.piece = p_obj
            squares.append(sq_ob)

    
    # Main gameplay loop
    running = True
    white = True
    current_piece = None
    current_square = None
    
    while running:
        
        # Check for events
        for event in pygame.event.get():
            
            mouse_pos = pygame.mouse.get_pos()

            # User closed window
            if event.type == pygame.QUIT:
                running = False

            # User clicked mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Click on piece
                for sq in squares:
                    if sq.piece:
                        if white and sq.piece.color == 'white' or not white and sq.piece.color == 'black':
                            if sq.piece.rect.collidepoint(mouse_pos):
                                current_piece = sq.piece
                                current_square = sq

            # User released mouse button
            if event.type == pygame.MOUSEBUTTONUP:
                if current_piece:
                    white = lock_piece(squares, current_piece, current_square, white)
                current_piece = None
                current_square = None

        # Moving pieces
        if current_piece:
            drag_piece(current_piece)
            
        # Draw on window
        draw_window(squares, PIECE_IMGS, white)       

    pygame.quit()


def draw_window(squares, images, white):

    # Set background color
    WINDOW.fill(PINK)
    
    # Draw squares
    for square in squares:
        if (square.location[0] + square.location[1]) % 2 == 0:
            pygame.draw.rect(WINDOW, ALMOND, square.rect)
        else:
            pygame.draw.rect(WINDOW, COFFEE, square.rect)

    # Draw header text
    if white:
        turn_text = "White to move..."
        header_text = FONT.render(turn_text, 1, WHITE)
    else:
        turn_text = "Black to move..."
        header_text = FONT.render(turn_text, 1, BLACK)

    WINDOW.blit(header_text, (WIDTH * .25, 10))

    # Draw pieces
    for square in squares:
        if square.piece:
            WINDOW.blit(images[square.piece.name], (square.piece.rect.x, square.piece.rect.y))

    pygame.display.update()


def drag_piece(piece):
    mouse_pos = pygame.mouse.get_pos()
    piece.rect.x = mouse_pos[0] - SQUARE_SIDE/2
    piece.rect.y = mouse_pos[1] - SQUARE_SIDE/2


def lock_piece(squares, piece, current_square, white):
    mouse_pos = pygame.mouse.get_pos()
    for sq in squares:
        if sq.rect.collidepoint(mouse_pos):

            # Invalid conditions
            if sq.piece:
                if sq.piece.color == piece.color:
                    break
            
            # Update Square data after lock succeeded
            for s in squares:
                if s.piece == piece:
                    s.piece = None
            sq.piece = piece
            
            # Update visual representation of piece
            piece.rect.x = sq.rect.x
            piece.rect.y = sq.rect.y
            return not white
    
    # Reset piece after lock failed
    piece.rect.x = current_square.location[1] * SQUARE_SIDE
    piece.rect.y = current_square.location[0] * SQUARE_SIDE + SQUARE_SIDE 
    return white

if __name__ == "__main__":
    main()