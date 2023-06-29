class Square:
    def __init__(self, location, rect, piece=None):
        self.location = location
        self.rect = rect
        self.piece = piece

class Piece:
    def __init__(self, name, color, rect=None):
        self.name = name
        self.color = color
        self.rect = rect
        self.moved = False

class Rook(Piece):
    def moves(self, location, squares):
        moves = []
        for sq in squares:
            if sq.location[0] == location[0] or sq.location[1] == location[1]:
                moves.append(sq)
        return moves
        

class Knight(Piece):
    def moves(self, squares):
        return

class Bishop(Piece):
    def moves(self, squares):
        return

class Queen(Piece):
    def moves(self, squares):
        return

class King(Piece):
    def moves(self, squares):
        return

class Pawn(Piece):
    def moves(self, location, squares):
        moves = []
        for sq in squares:

            # Moving one square forward
            if sq.location[0] == location[0] - 1 and sq.location[1] == location[1]:
                moves.append(sq)

            # Moving two squares if first move
            if self.moved == False:
                if sq.location[0] == location[0] - 2 and sq.location[1] == location[1]:
                    moves.append(sq)

            # Capture
            if sq.piece:
                if sq.piece.color != self.color:
                    if sq.location[0] == location[0] - 1 and sq.location[1] in [location[1] - 1, location[1] + 1]:
                        moves.append(sq)
        return moves