import pygame

# Set window dimensions & caption
WIDTH, HEIGHT = 512, 640
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Set square dimensions
SQUARE_SIDE = WIDTH/8

# RGB color values
PINK = (234, 202, 252)
ALMOND = (234, 221, 202)
COFFEE = (111, 78, 55)

# Initialize 2D array of tuples to create board
SQUARES = []
for i in range(8):
    row = []
    for j in range(8):
        square = (i, j)
        row.append(square)
    SQUARES.append(row)


def main():
    
    running = True
    # Main gameplay loop
    while running:
        
        # Check for events
        for event in pygame.event.get():
            
            # User closed window
            if event.type == pygame.QUIT:
                running = False

    
        draw_window()        

    pygame.quit()


def draw_window():

    WINDOW.fill(PINK)
    
    # Draw squares
    for row in SQUARES:
        for square in row:
            sq_rect = pygame.Rect((square[1] * 64), (square[0] * 64 + 64), SQUARE_SIDE, SQUARE_SIDE)
            
            if (square[0] + square[1]) % 2 == 0:
                pygame.draw.rect(WINDOW, ALMOND, sq_rect)
            else:
                pygame.draw.rect(WINDOW, COFFEE, sq_rect)
                



    pygame.display.update()

if __name__ == "__main__":
    main()