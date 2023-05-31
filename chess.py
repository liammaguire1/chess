import pygame
import os

from pieces import *

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

    # Create square dicts
    for row in SQUARES:
        for square in row:
            
            # Square rect
            sq_rect = pygame.Rect((square[1] * SQUARE_SIDE), (square[0] * SQUARE_SIDE + SQUARE_SIDE), SQUARE_SIDE, SQUARE_SIDE)

            # Dict to be appended to 'squares' list
            sq_dict = {}
            sq_dict['location'] = square
            sq_dict['sq_rect'] = sq_rect
            
            # Initial placement of pieces
            if square in [(0,0), (0,7)]:
                sq_dict['piece'] = 'black-rook'
            elif square in [(0,1), (0,6)]:
                sq_dict['piece'] = 'black-knight'
            elif square in [(0,2), (0,5)]:
                sq_dict['piece'] = 'black-bishop'
            elif square == (0, 3):
                sq_dict['piece'] = 'black-queen'
            elif square == (0, 4):
                sq_dict['piece'] = 'black-king'
            elif square[0] == 1:
                sq_dict['piece'] = 'black-pawn'
            elif square in [(7,0), (7,7)]:
                sq_dict['piece'] = 'white-rook'
            elif square in [(7,1), (7,6)]:
                sq_dict['piece'] = 'white-knight'
            elif square in [(7,2), (7,5)]:
                sq_dict['piece'] = 'white-bishop'
            elif square == (7, 3):
                sq_dict['piece'] = 'white-queen'
            elif square == (7, 4):
                sq_dict['piece'] = 'white-king'
            elif square[0] == 6:
                sq_dict['piece'] = 'white-pawn'
            else:
                sq_dict['piece'] = None

            # Create Rect for pieces
            if sq_dict['piece']:
                sq_dict['piece_rect'] = pygame.Rect(sq_dict['location'][1] * SQUARE_SIDE, sq_dict['location'][0] * SQUARE_SIDE + SQUARE_SIDE, PIECE_SIZE, PIECE_SIZE)
            else:
                sq_dict['piece_rect'] = None

            # Append dict to list of all squares
            squares.append(sq_dict)

    
    # Main gameplay loop
    running = True
    white = True
    piece = None
    
    while running:
        
        # Check for events
        for event in pygame.event.get():
            
            mouse_pos = pygame.mouse.get_pos()

            # User closed window
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Click on piece
                for sq in squares:
                    if sq['piece_rect']:
                        if sq['piece_rect'].collidepoint(mouse_pos):
                            piece = sq['piece_rect']

            if event.type == pygame.MOUSEBUTTONUP:
                if piece:
                    lock_piece(piece)
                piece = None

        # Clicking pieces
        if piece:
            drag_piece(piece)
            
        # Draw on window
        draw_window(squares, PIECE_IMGS)       

    pygame.quit()


def draw_window(squares, images):

    # Set background color
    WINDOW.fill(PINK)
    
    # Draw squares
    for square in squares:
        if (square['location'][0] + square['location'][1]) % 2 == 0:
            pygame.draw.rect(WINDOW, ALMOND, square['sq_rect'])
        else:
            pygame.draw.rect(WINDOW, COFFEE, square['sq_rect'])

    # Draw pieces
    for square in squares:
        if square['piece']:
            WINDOW.blit(images[square['piece']], (square['piece_rect'].x, square['piece_rect'].y))

    pygame.display.update()


def drag_piece(piece):
    mouse_pos = pygame.mouse.get_pos()
    piece.x = mouse_pos[0] - SQUARE_SIDE/2
    piece.y = mouse_pos[1] - SQUARE_SIDE/2


def lock_piece(piece):
    return


if __name__ == "__main__":
    main()