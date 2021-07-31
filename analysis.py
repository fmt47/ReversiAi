"""CSC111 Final Project: AI Player for Reversi

Instructions:
This Python module contains the evaluation method to find
how well an AI player performs.

Copyright and Usage Information:
This file is Copyright (c) 2021 Yupeng Chang, Huiru Tan, Xi Chen.
"""
import plotly.graph_objects as go
import plotly
from reversi_board import Reversi
from reversi_player import Player, RandomPlayer, MiniMaxPlayer, \
    evaluate_score_by_piece, evaluate_score_by_position
import random

# The game simulate takes time to run
# These are statics data of the result
minimax_black_random_white = {'TOTAL': 10, 'BLACK PLAYER': 10, 'WHITE PLAYER': 0, 'TIE': 0}
minimax_white_random_black = {'TOTAL': 10, 'BLACK PLAYER': 10, 'WHITE PLAYER': 0, 'TIE': 0}


def get_performance(test_player: Player, n: int) -> float:
    """simulate game for n times
    get the performance of the player
    which is calculate by (win + (tie/2))/n"""
    # result = {'BLACK PLAYER': 0, 'WHITE PLAYER': 0, 'TIE': 0}
    result = {'random': 0, 'test_player': 0, 'tie': 0}
    players = [RandomPlayer(Reversi()), test_player]
    for i in range(n):
        random.shuffle(players)
        player_info = {'BLACK PLAYER': 'test_player', 'WHITE PLAYER': 'random', 'TIE': 'tie'}

        if players[1] is test_player:
            player_info['WHITE PLAYER'] = 'test_player'
            player_info['BLACK PLAYER'] = 'random'

        game = Reversi()
        winner = run_one_simulate(game, players[0], players[1])
        result[player_info[winner]] += 1
        print(f'{i + 1}', end='')
    return (result['test_player'] + result['tie'] / 2) / n


def run_one_simulate(game: Reversi, black_player: Player, white_player: Player):
    """simulate game once and return the winner"""
    black_player.game = game
    white_player.game = game
    while game.winner() is None:
        if game.is_black_move:
            game.make_move(black_player.think_move())
        else:
            game.make_move(white_player.think_move())
    return game.winner()


def plot_data(depth: int, n: int) -> None:
    """
    plot the line graph to compare the performance
    of minimax players with two difference game score
    evaluation methods. n is the number of games
    """
    depth = list(range(1, depth + 1))
    random_evaluate = []
    simple_evaluate = []
    position_evaluate = []
    for d in depth:
        print(f'depth is {d}')
        random_player = RandomPlayer(Reversi())
        simple_minimax = MiniMaxPlayer(Reversi(), d, 99, evaluate_score_by_piece)
        complex_minimax = MiniMaxPlayer(Reversi(), d, 99, evaluate_score_by_position)

        random_evaluate.append(get_performance(random_player, n))
        simple_evaluate.append(get_performance(simple_minimax, n))
        position_evaluate.append(get_performance(complex_minimax, n))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=depth, y=random_evaluate,
                             mode='lines+markers',
                             name='random player'))

    fig.add_trace(go.Scatter(x=depth, y=simple_evaluate,
                             mode='lines+markers',
                             name='simple computer'))

    fig.add_trace(go.Scatter(x=depth, y=position_evaluate,
                             mode='lines+markers',
                             name='complex computer'))
    with open('plot.html', 'w') as plot_file:
        print(plotly.io.to_html(fig), file=plot_file)
    fig.show()


if __name__ == '__main__':
    random1 = RandomPlayer(Reversi())
    random2 = RandomPlayer(Reversi())
    print('Simulate one game between two random player,\n'
          f'the winner is {run_one_simulate(Reversi(), random1, random2)}')

    # uncomment function below to see comparision of the performance score
    # of simple minimax player and complex minimax player, when the depth
    # of game tree is 1, and 2, with 10 games.
    # takes about 1 min.

    # plot_data(2, 10)
