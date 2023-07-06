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
        moves += self.vision(squares, (current_square[0] - 2, current_square[1] - 1))
        moves += self.vision(squares, (current_square[0] - 2, current_square[1] + 1))
        moves += self.vision(squares, (current_square[0] + 2, current_square[1] - 1))
        moves += self.vision(squares, (current_square[0] + 2, current_square[1] + 1))
        moves += self.vision(squares, (current_square[0] - 1, current_square[1] - 2))
        moves += self.vision(squares, (current_square[0] + 1, current_square[1] - 2))
        moves += self.vision(squares, (current_square[0] - 1, current_square[1] + 2))
        moves += self.vision(squares, (current_square[0] + 1, current_square[1] + 2))
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
        return moves

class Pawn(Piece):
    def moves(self, location, squares):
        moves = []
        for sq in squares:
            
            # Moving one square forward
            if sq[0] == location[0] - 1 and sq[1] == location[1]:
                moves.append(sq)

            # Moving two squares if first move
            if self.moved == False:
                if sq[0] == location[0] - 2 and sq[1] == location[1]:
                    moves.append(sq)

            # Capture
            if squares[sq].piece:
                if squares[sq].piece.color != self.color:
                    if sq[0] == location[0] - 1 and sq[1] in [location[1] - 1, location[1] + 1]:
                        moves.append(sq)
        return moves