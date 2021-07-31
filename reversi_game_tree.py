"""CSC111 Final Project: AI Player for Reversi

Instructions:
This Python module contains the game tree of Reversi

Copyright and Usage Information:
This file is Copyright (c) 2021 Yupeng Chang, Huiru Tan, Xi Chen.
"""
START = '*'


class GameTree:
    """
    The class represent a valid move in the game.

    Instance Attributes:
        - move: a valid move in the game
        - score: the evaluation score of the game board for
            black player or white player after the move is made
        - is_black_move: true iff the next player is black player
        - sub_trees: a list of possible moves after the self.move is made
    """
    move: tuple[int]
    score: int
    is_black_move: bool
    sub_trees: list

    def __init__(self, move: any, is_black_move: bool, score: int = 0) -> None:
        self.move = move
        self.score = score
        self.is_black_move = is_black_move
        self.sub_trees = []

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self.str_indented(0)

    def str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.
        The indentation level is specified by the <depth> parameter.
        modified from a2
        """
        if self.is_black_move:
            turn_desc = "Black"
        else:
            turn_desc = "White"
        move_desc = f'{self.move} [{self.score}] -> {turn_desc}\n'
        s = '  ' * depth + move_desc
        if self.sub_trees == []:
            return s
        else:
            for subtree in self.sub_trees:
                s += subtree.str_indented(depth + 1)
            return s

    def add_subtree(self, subtree: any) -> None:
        """add a new move after self.move"""
        self.sub_trees.append(subtree)

    def find_subtree_by_move(self, move: tuple) -> any:
        """return the subtree that subtree.move == move"""
        for s in self.sub_trees:
            if s.move == move:
                return s
        return None


if __name__ == '__main__':
    g = GameTree(START, True)
    g2 = GameTree((1, 2), False, 9)
    g3 = GameTree((4, 4), False, 7)
    g.add_subtree(g2)
    g.add_subtree(g3)
    print(g)
