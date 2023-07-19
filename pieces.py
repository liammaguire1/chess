class Square:
    def __init__(self, rect, piece=None):
        self.rect = rect
        self.piece = piece

class Piece:
    def __init__(self, name, color, rect=None):
        self.name = name
        self.color = color
        self.rect = rect
        self.moved = False

class Rook(Piece):
    def vision(self, squares, direction, key, iter, vert=False):
        moves = []
        while direction in range(8):
            if vert:
                k = (direction, key)
            else:
                k = (key, direction)

            if squares[k].piece:
                if squares[k].piece.color != self.color:
                    moves.append(k)
                    break
                else:
                    break
            else:
                moves.append(k)
            direction += iter
        return moves

    def moves(self, current_square, squares):
        moves = []
        
        # TODO make pretty
        # Down
        moves += self.vision(squares, current_square[0] + 1, current_square[1], 1, vert=True)
        # Up
        moves += self.vision(squares, current_square[0] - 1, current_square[1], -1, vert=True)
        # Left
        moves += self.vision(squares, current_square[1] - 1, current_square[0], -1)
        # Right
        moves += self.vision(squares, current_square[1] + 1, current_square[0], 1)
        return moves

class Knight(Piece):
    def vision(self, squares, square):
        if square[0] in range(8) and square[1] in range(8):
            if squares[square].piece:
                if squares[square].piece.color != self.color:
                    return [square]
            else:
                return [square]
        return []
    
    def moves(self, current_square, squares):
        moves = []
        
        # TODO make pretty
        #for i in range(8):
        #    print(i % 2 + 1)
            
        moves += self.vision(squares, (current_square[0] - 1, current_square[1] - 2))
        moves += self.vision(squares, (current_square[0] + 1, current_square[1] - 2))
        moves += self.vision(squares, (current_square[0] - 1, current_square[1] + 2))
        moves += self.vision(squares, (current_square[0] + 1, current_square[1] + 2))
        moves += self.vision(squares, (current_square[0] - 2, current_square[1] - 1))
        moves += self.vision(squares, (current_square[0] + 2, current_square[1] - 1))
        moves += self.vision(squares, (current_square[0] - 2, current_square[1] + 1))
        moves += self.vision(squares, (current_square[0] + 2, current_square[1] + 1))
        return moves

class Bishop(Piece):
    def vision(self, squares, i, j, i_iter, j_iter):
        moves = []
        while i in range(8) and j in range(8):
            if squares[(i, j)].piece:
                if squares[(i, j)].piece.color != self.color:
                    moves.append((i, j))
                    break
                else:
                    break
            else:
                moves.append((i, j))
            i += i_iter
            j += j_iter
        return moves

    def moves(self, current_square, squares):
        moves = []

        # TODO make pretty
        # Up-left
        moves += self.vision(squares, current_square[0] - 1, current_square[1] - 1, -1, -1)
        # Up-right
        moves += self.vision(squares, current_square[0] - 1, current_square[1] + 1, -1, 1)
        # Down-left
        moves += self.vision(squares, current_square[0] + 1, current_square[1] - 1, 1, -1)
        # Down-right
        moves += self.vision(squares, current_square[0] + 1, current_square[1] + 1, 1, 1)
        return moves

class Queen(Piece):
    def moves(self, current_square, squares):
        moves = []
        bishop = Bishop(name='bishop', color=self.color)
        rook = Rook(name='rook', color=self.color)
        moves += bishop.moves(current_square, squares) + rook.moves(current_square, squares)
        return moves

class King(Piece):
    def moves(self, current_square, squares):
        moves = []
        # Normal movement
        for i in range(-1, 2):
            for j in range(-1, 2):
                if current_square[0] + i in range(8) and current_square[1] + j in range(8):
                    if squares[(current_square[0] + i, current_square[1] + j)].piece:
                        if squares[(current_square[0] + i, current_square[1] + j)].piece.color == self.color:
                            continue
                    moves.append((current_square[0] + i, current_square[1] + j))

        # Castling
        if self.moved == False:
            for i in range(-1, 2, 2):
                j = current_square[1]
                while j in range(1, 7):
                    if squares[(7, j + i)].piece:
                        if type(squares[(7, j + i)].piece) == Rook and squares[(7, j + i)].piece.color == self.color and squares[(7, j + i)].piece.moved == False:
                            moves.append((7, current_square[1] + (i * 2))) 
                        else:
                            break
                    j = j + i
        return moves

class Pawn(Piece):
    def moves(self, current_square, squares, played_moves):
        moves = []
        # Move one square forward
        if not squares[(current_square[0] - 1, current_square[1])].piece:
            moves.append((current_square[0] - 1, current_square[1]))
            # Move two squares forward
            if self.moved == False:
                if not squares[(current_square[0] - 2, current_square[1])].piece:
                    moves.append((current_square[0] - 2, current_square[1]))

        # Capture
        for i in range(-1, 2, 2):
            if current_square[0] - 1 in range(8) and current_square[1] + i in range(8):
                if squares[(current_square[0] - 1, current_square[1] + i)].piece:
                    if squares[(current_square[0] - 1, current_square[1] + i)].piece.color != self.color:
                        moves.append((current_square[0] - 1, current_square[1] + i))

        # En passant
        if len(played_moves) > 0:
            if type(played_moves[-1][0]) == Pawn and played_moves[-1][1][0] == 6 and played_moves[-1][2][0] == 4 and abs((7 - played_moves[-1][1][1]) - current_square[1]) == 1 and current_square[0] == 3:
                moves.append((2, 7 - played_moves[-1][2][1]))
        return moves