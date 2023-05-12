import pygame
import os

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

FPS = 60

def main():

    clock = pygame.time.Clock()
    
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
            sq_dict['rect'] = sq_rect
            
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

            squares.append(sq_dict)

    
    # Main gameplay loop
    running = True
    while running:
        
        # Set FPS
        clock.tick(FPS)

        # Check for events
        for event in pygame.event.get():
            
            # User closed window
            if event.type == pygame.QUIT:
                running = False

            # User clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                square_click(squares)

        
    
        draw_window(squares, PIECE_IMGS)       

    pygame.quit()


def draw_window(squares, images):

    # Set background color
    WINDOW.fill(PINK)
    
    # Draw squares
    for square in squares:

            # Checkered coloring
            if (square['location'][0] + square['location'][1]) % 2 == 0:
                pygame.draw.rect(WINDOW, ALMOND, square['rect'])
            else:
                pygame.draw.rect(WINDOW, COFFEE, square['rect'])

            if square['piece']:
                WINDOW.blit(images[square['piece']], (square['location'][1] * SQUARE_SIDE, square['location'][0] * SQUARE_SIDE + SQUARE_SIDE))
                

    pygame.display.update()


def square_click(squares, first=True):
    mouse = pygame.mouse.get_pos()
    for sq in squares:
        if sq['rect'].collidepoint(mouse):
            print(sq['location'])


if __name__ == "__main__":
    main()