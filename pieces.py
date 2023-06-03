class Square:
    def __init__(self, location, rect, piece=None):
        self.location = location
        self.rect = rect
        self.piece = piece

class Piece:
    def __init__(self, name, white, rect=None):
        self.name = name
        self.white = white
        self.rect = rect
        self.moved = False

class Rook(Piece):
    def moves(self):
        return

class Knight(Piece):
    def moves(self):
        return

class Bishop(Piece):
    def moves(self):
        return

class Queen(Piece):
    def moves(self):
        return

class King(Piece):
    def moves(self):
        return

class Pawn(Piece):
    def moves(self):
        return