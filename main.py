from easyAI import TwoPlayerGame
from easyAI.Player import Human_Player

from Pieces import Pieces
from PawnMove import PawnMove

class Quarto( TwoPlayerGame ):
    """ explain game rules here. Probably """
    def __init__(self, players):
        self.players = players
        self.pawnsPile = Pieces().pawns
        self.board = [[None for _ in range(4)] for _ in range(4)]
        self.current_player = 1
    
    def possible_moves(self):
        moves = []
        for row in range(4):
            for col in range(4):
                if self.board[row][col] is None:
                    empty_position = (row, col)
                    for index, pawn in enumerate(self.pawnsPile):
                        # moves.append((empty_position, (index, pawn)))
                        move = PawnMove(empty_position, index, pawn)
                        moves.append(move)
        return moves

    def make_move(self, move): 
        row_pos = move.position[0]
        col_pos = move.position[1]
        index = move.index
        pawn = move.pawn
        self.board[row_pos][col_pos] = pawn
        self.pawnsPile.pop(index)

    def unmake_move(self, move):
        row_pos = move.position[0]
        col_pos = move.position[1]
        index = move.index
        pawn = move.pawn
        self.board[row_pos][col_pos] = None
        self.pawnsPile.insert(index, pawn)

    def lose(self):
        """ When player lose """
        # check for vertical lines
        for col in range(4):
            if (
                self.board[0][col]
                and self.board[0][col] == self.board[1][col]
                and self.board[0][col] == self.board[2][col]
                and self.board[0][col] == self.board[3][col]
            ):
                if self.has_common_attribute_in_vertical_line(0, col, "size"):
                    return True
                if self.has_common_attribute_in_vertical_line(0, col, "color"):
                    return True
                if self.has_common_attribute_in_vertical_line(0, col, "shape"):
                    return True
                if self.has_common_attribute_in_vertical_line(0, col, "hollow"):
                    return True
            
        # check for horizontal lines
        for row in range(4):
            if (
                self.board[row][0]
                and self.board[row][0] == self.board[row][1]
                and self.board[row][0] == self.board[row][2]
                and self.board[row][0] == self.board[row][3]
            ):
                if self.has_common_attribute_in_horizontal_line(row, 0, "size"):
                    return True
                if self.has_common_attribute_in_horizontal_line(row, 0, "color"):
                    return True
                if self.has_common_attribute_in_horizontal_line(row, 0, "shape"):
                    return True
                if self.has_common_attribute_in_horizontal_line(row, 0, "hollow"):
                    return True
                
        # check for first diagonal line
        if (
            self.board[0][0]
            and self.board[0][0] == self.board[1][1]
            and self.board[0][0] == self.board[2][2]
            and self.board[0][0] == self.board[3][3]
        ):
            if self.has_common_attribute_in_diagonal_line_1("size"):
                return True
            if self.has_common_attribute_in_diagonal_line_1("color"):
                return True
            if self.has_common_attribute_in_diagonal_line_1("shape"):
                return True
            if self.has_common_attribute_in_diagonal_line_1("hollow"):
                return True

        # check for second diagonal line
        if (
            self.board[3][0]
            and self.board[3][0] == self.board[2][1]
            and self.board[3][0] == self.board[1][2]
            and self.board[3][0] == self.board[0][3]
        ):
            if self.has_common_attribute_in_diagonal_line_2("size"):
                return True
            if self.has_common_attribute_in_diagonal_line_2("color"):
                return True
            if self.has_common_attribute_in_diagonal_line_2("shape"):
                return True
            if self.has_common_attribute_in_diagonal_line_2("hollow"):
                return True

    def has_common_attribute_in_vertical_line(self, row, col, attribute):
        common_value = self.board[row][col].__dict__[attribute]
        return all(
            self.board[row + i][col] is not None
            and self.board[row + i][col].__dict__[attribute] == common_value
            for i in range(4)
        )
    
    def has_common_attribute_in_horizontal_line(self, row, col, attribute):
        common_value = self.board[row][col].__dict__[attribute]
        return all(
            self.board[row][col + i] is not None
            and self.board[row][col + i].__dict__[attribute] == common_value
            for i in range(4)
        )

    def has_common_attribute_in_diagonal_line_1(self, attribute):
        common_value = self.board[0][0].__dict__[attribute]
        return all(
            self.board[0 + i][0 + i] is not None
            and self.board[0 + i][0 + i].__dict__[attribute] == common_value
            for i in range(4)
        )
    
    def has_common_attribute_in_diagonal_line_2(self, attribute):
        common_value = self.board[3][0].__dict__[attribute]
        return all(
            self.board[3 - i][0 + i] is not None
            and self.board[3 - i][0 + i].__dict__[attribute] == common_value
            for i in range(4)
        )

    def is_over(self): return (self.possible_moves() == []) or self.lose()
    def scoring(self): return -100 if self.lose() else 0

    def show(self): 
        print ("Pawns in the pool:")
        for pawn in self.pawnsPile:
            print(pawn, end=" ")
        print()
        print("Board")
        for row in self.board: 
            for pawn in row: 
                if pawn is None: 
                    print(" .", end="")
                else:
                    print(pawn, end="")
            print()
        print("Type 'show moves to see all moves")
        print("To move a pawn type e.g. 'move #11'")

# if __name__ == "__main__":
#     from easyAI import TranspositionTable, solve_with_iterative_deepening
    
#     tt = TranspositionTable()
#     Quarto.ttentry = lambda game : game.pawnsPile

#     result, depth, move = solve_with_iterative_deepening(
#                 game=Quarto(),
#                 ai_depths=range(7,16),
#                 win_score=100,
#                 tt=tt
#             )
#     game = Quarto( [ AI_Player(tt), Human_Player() ] )
#     game.play()

if __name__ == "__main__":
    from easyAI import AI_Player, Negamax

    ai = Negamax(5)
    game = Quarto( [ Human_Player(), AI_Player(ai) ] )
    history = game.play()