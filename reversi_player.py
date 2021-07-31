"""CSC111 Final Project: AI Player for Reversi

Instructions:
This Python module contains the Minimax AI players and
different evaluation function for getting the potential
of a certain board situation

Copyright and Usage Information:
This file is Copyright (c) 2021 Yupeng Chang, Huiru Tan, Xi Chen.
"""
from reversi_board import Reversi, WHITE_PIECE, BLACK_PIECE
import random
from reversi_game_tree import GameTree, START
import time

WEIGHT = [[5, 1, 2, 2, 2, 2, 1, 5],
          [1, 1, 1, 1, 1, 1, 1, 1],
          [2, 1, 2, 1, 1, 2, 1, 2],
          [2, 1, 1, 1, 1, 1, 1, 2],
          [2, 1, 1, 1, 1, 1, 1, 2],
          [2, 1, 2, 1, 1, 2, 1, 2],
          [1, 1, 1, 1, 1, 1, 1, 1],
          [5, 1, 2, 2, 2, 2, 1, 5]]


class Player:
    """The abstract class of player"""

    game: Reversi

    def __init__(self, game: Reversi) -> None:
        """Initialize the player"""
        self.game = game

    def think_move(self) -> tuple[int]:
        """Think a new move based on current situation"""
        raise NotImplementedError


class RandomPlayer(Player):
    """The player who make random move"""

    def think_move(self) -> tuple[int]:
        """random choose a new move"""
        return random.choice(self.game.valid_moves)


class MiniMaxPlayer(Player):
    """The player follow Minimax Algorithm

    Instance Attributes:
        - game: the reversi game
        - depth: the depth of the game tree for making best move
        - think_time: maximum time to generate game tree in seconds.
        - evaluate_algorithm: the evaluation function for AI player to
            understand the situation of the board.
    """

    game: Reversi
    depth: int
    think_time: int
    evaluate_algorithm: callable

    def __init__(self, game: Reversi, depth: int, think_time: int, evaluate: callable) -> None:
        """Initialize the player"""
        super().__init__(game)
        self.think_time = think_time
        self.depth = depth
        self.evaluate_algorithm = evaluate

    def generate_tree(self) -> GameTree:
        """get full tree of moves"""
        start_time = time.time()
        return generate_game_tree(START,
                                  self.game,
                                  self.depth,
                                  start_time,
                                  self.think_time,
                                  self.game.is_black_move,
                                  self.evaluate_algorithm)

    def think_move(self) -> tuple[int]:
        """Make move by minimax algorithm"""
        game_tree = self.generate_tree()
        apply_minimax(game_tree, game_tree.is_black_move)
        if game_tree.sub_trees != []:
            score = game_tree.score
            for s in game_tree.sub_trees:
                if s.score == score:
                    # print('MiniMax Player though 1 move')
                    return s.move
        return random.choice(self.game.valid_moves)


def apply_minimax(game_tree: GameTree, is_black_move: bool) -> None:
    """calculate score of each game tree by minimax algorithm and evaluate function"""
    if game_tree.sub_trees != []:
        for s in game_tree.sub_trees:
            apply_minimax(s, is_black_move)
        if game_tree.is_black_move == is_black_move:
            game_tree.score = max(s.score for s in game_tree.sub_trees)
        else:
            game_tree.score = min(s.score for s in game_tree.sub_trees)


def generate_game_tree(move: any,
                       game: Reversi,
                       depth: int,
                       start_time: float,
                       think_time: int,
                       is_black_move: bool,
                       evaluate: callable) -> GameTree:
    """generate game tree with all moves but no score
    the maximum think time is think_time"""
    game_tree = GameTree(move, game.is_black_move, evaluate(game, is_black_move))

    if time.time() - start_time < think_time and depth > 0:
        for move in game.get_valid_moves():
            sub_game = game.copy_board()
            sub_game.make_move(move)
            game_tree.add_subtree(generate_game_tree(move,
                                                     sub_game,
                                                     depth - 1,
                                                     start_time,
                                                     think_time,
                                                     is_black_move,
                                                     evaluate))
    return game_tree


def evaluate_score_by_piece(game: Reversi, for_black: bool) -> int:
    """simple return the difference of the score"""
    if for_black:
        return game.black_score - game.white_score
    return game.white_score - game.black_score


def evaluate_score_by_position(game: Reversi, for_black: bool) -> int:
    """return the weighted score difference
    """
    black_score = 0
    white_score = 0
    for row in range(8):
        for column in range(8):
            if game.board[row][column] == BLACK_PIECE:
                black_score += WEIGHT[row][column]
            if game.board[row][column] == WHITE_PIECE:
                white_score += WEIGHT[row][column]

    if for_black:
        return black_score - white_score
    return white_score - black_score


if __name__ == '__main__':
    from pprint import pprint
    r = Reversi([[2, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 2, 1, 0, 0, 0],
                 [0, 0, 0, 1, 2, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])
    print('A special case of the board')
    pprint(r.board)
    print(f'the evaluation score for black of equal weigh is 3 - 2'
          f' = {evaluate_score_by_piece(r, True)}')
    print(f'According to the constant WEIGHT at the top of the page,\n'
          f'the evaluation score for black of different weigh is 2 * 1 + 1 * 5 - 2 * 1'
          f' = {evaluate_score_by_position(r, True)}')
