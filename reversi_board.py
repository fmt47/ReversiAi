"""CSC111 Final Project: AI Player for Reversi

Instructions:
This Python module contains the game board and rules of Reversi

Copyright and Usage Information:
This file is Copyright (c) 2021 Yupeng Chang, Huiru Tan, Xi Chen.
"""
import copy

BLACK_PIECE = 2
WHITE_PIECE = 1
EMPTY_PIECE = 0


class Reversi:
    """The class represents a Reversi game

    Instance Attributes:
        - board: the nest list represent the game board, the elements
            are WHITE_PIECE, BLACK_PIECE, and EMPTY_PIECE.
        - valid_moves: the list of valid moves of current player
        - is_black_move: true iff current player is black player
        - white_score: the number of WHITE_PIECE in self.board
        - black_score: the number of BLACK_PIECE on self.board
    """
    board: list[list[any]]
    valid_moves: list[tuple]
    is_black_move: bool
    white_score: int
    black_score: int

    def __init__(self, board=None, is_black_move=True) -> None:
        """Initialize the board, update the valid_moves iff not for testing
        to avoid recursion error"""
        if board is None:
            board = [[EMPTY_PIECE] * 8 for _ in range(8)]
            board[3][3], board[4][4], board[3][4], board[4][3] = \
                BLACK_PIECE, BLACK_PIECE, WHITE_PIECE, WHITE_PIECE
        self.board = board
        self.is_black_move = is_black_move
        self.valid_moves = []
        self.valid_moves = self.get_valid_moves()
        self.update_score()

    def winner(self) -> any:
        """return None is game is not end, otherwise return the winner"""
        if self.valid_moves == []:
            if self.black_score > self.white_score:
                return 'BLACK PLAYER'
            if self.black_score < self.white_score:
                return 'WHITE PLAYER'
            return 'TIE'
        return None

    def update_score(self) -> None:
        """update the scores"""
        self.white_score = len([0 for row in range(8) for column in range(8) if
                                self.board[row][column] == WHITE_PIECE])
        self.black_score = len([0 for row in range(8) for column in range(8) if
                                self.board[row][column] == BLACK_PIECE])

    def get_valid_moves(self) -> list[tuple]:
        """return valid moves"""
        valid_moves = []
        for row in range(8):
            for column in range(8):
                if self.is_valid_move(row, column):
                    valid_moves.append((row, column))
        return valid_moves

    def make_move(self, move: tuple) -> None:
        """make move and update valid moves"""
        if move not in self.valid_moves:
            raise ValueError
        self.update_board(move[0], move[1])
        self.update_score()
        self.is_black_move = not self.is_black_move
        self.valid_moves = self.get_valid_moves()

    def is_valid_move(self, row, column) -> bool:
        """return true iff the move is at empty grid
         and reverse at least one piece"""
        if self.board[row][column] != EMPTY_PIECE:
            return False
        return self.update_board(row, column, for_test=True) > 0

    def update_board(self, row: int, column: int, for_test: bool = False) -> int:
        """get the nearest piece of a new piece
        then update board and return the number of piece change"""

        # not change the board when testing the validation
        if not for_test:
            self.board[row][column] = self.next_piece()

        total_reverse = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d in directions:
            pos = [row + d[0], column + d[1]]  # the position
            viewed_pos = []
            should_continue = True

            while all(0 <= x <= 7 for x in pos) and should_continue:
                if self.board[pos[0]][pos[1]] == EMPTY_PIECE:
                    should_continue = False
                elif self.board[pos[0]][pos[1]] != self.next_piece():
                    viewed_pos.append((pos[0], pos[1]))
                else:
                    # not change the board when testing the validation
                    if len(viewed_pos) != 0 and not for_test:
                        for v in viewed_pos:
                            self.board[v[0]][v[1]] = self.next_piece()
                    total_reverse += len(viewed_pos)
                    should_continue = False
                pos[0] += d[0]
                pos[1] += d[1]

        return total_reverse

    def copy_board(self, is_black_move=None) -> any:
        """Return the game with same board"""
        if is_black_move is None:
            return Reversi(copy.deepcopy(self.board), self.is_black_move)
        return Reversi(copy.deepcopy(self.board), is_black_move)

    def next_piece(self) -> any:
        """Return the piece of next player"""
        if self.is_black_move:
            return BLACK_PIECE
        return WHITE_PIECE


if __name__ == '__main__':
    from pprint import pprint
    r = Reversi()
    print('this is the initial board')
    pprint(r.board)
    print(f'black score is {r.black_score}, white score is {r.white_score}')
    print('valid move for black is', r.valid_moves)
    print('Now black make move at row 3, column 5')
    r.make_move((2, 4))
    print('one white piece at row 4 column 5 is reversed to black')
    print('now the board is')
    pprint(r.board)
    print(f'black score is {r.black_score}, white score is {r.white_score}')
