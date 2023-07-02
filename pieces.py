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
    def vision(self, i, j)
    
    def moves(self, current_square, squares):
        moves = []
        
        # Right
        i = current_square[0] + 1
        while i >= 0 and i <= 7:
            if squares[(i, current_square[1])].piece:
                if squares[(i, current_square[1])].piece.color != self.color:
                    moves.append((i, current_square[1]))
                    break
                else:
                    break
            else:
                moves.append((i, current_square[1]))
            i += 1
                
        # Left
        i = current_square[0] - 1
        while i >= 0 and i <= 7:
            if squares[(i, current_square[1])].piece:
                if squares[(i, current_square[1])].piece.color != self.color:
                    moves.append((i, current_square[1]))
                    break
                else:
                    break
            else:
                moves.append((i, current_square[1]))
            i -= 1

        # Up
        j = current_square[1] - 1
        while j >= 0 and j <= 7:
            if squares[(current_square[0], j)].piece:
                if squares[(current_square[0], j)].piece.color != self.color:
                    moves.append((current_square[0], j))
                    break
                else:
                    break
            else:
                moves.append((current_square[0], j))
            j -= 1

        # Down
        j = current_square[1] + 1
        while j >= 0 and j <= 7:
            if squares[(current_square[0], j)].piece:
                if squares[(current_square[0], j)].piece.color != self.color:
                    moves.append((current_square[0], j))
                    break
                else:
                    break
            else:
                moves.append((current_square[0], j))
            j += 1
        print(moves)
        return moves
        

class Knight(Piece):
    def moves(self, current_square, squares):
        moves = []
        return moves

class Bishop(Piece):
    def moves(self, current_square, squares):
        moves = []
        return moves

class Queen(Piece):
    def moves(self, current_square, squares):
        moves = []
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