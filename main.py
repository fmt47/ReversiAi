"""CSC111 Final Project: AI Player for Reversi

Instructions:
This Python module contains the user interface of the project
which contain three mode,
VS Mode: Set players for black and white then play game
Analysis Mode: Human can make moves and see the live displayed
    potential score of each possible move
Evaluation Mode: Plot and compare the performance score of
    simple minimax player and complex minimax player.

Copyright and Usage Information:
This file is Copyright (c) 2021 Yupeng Chang, Huiru Tan, Xi Chen.
"""
from tkinter import ttk
import tkinter as tk
from reversi_board import Reversi
from reversi_pygame import run_game, analysis_game
from reversi_player import RandomPlayer, MiniMaxPlayer, \
    evaluate_score_by_piece, evaluate_score_by_position
from analysis import plot_data


def compare_performance() -> None:
    """plot performance"""
    n = menu4.get()
    depth = menu5.get()
    plot_data(int(depth), int(n))


def start_analysis() -> None:
    """start analysis mode"""
    game = Reversi()
    print('new game')
    analysis_game(game)


def start_game() -> None:
    """start a new game"""
    black_player = menu1.get()
    white_player = menu2.get()
    depth = int(menu3.get())
    print(black_player, white_player, depth)
    info = [black_player, white_player, depth]
    game = Reversi()

    if white_player == 'Random Computer':
        white_player = RandomPlayer(game)
    elif white_player == 'Simple Computer':
        white_player = MiniMaxPlayer(game, depth, 99, evaluate_score_by_piece)
    elif white_player == 'Complex Computer':
        white_player = MiniMaxPlayer(game, depth, 99, evaluate_score_by_position)
    else:
        white_player = 'HUMAN'

    if black_player == 'Random Computer':
        black_player = RandomPlayer(game)
    elif black_player == 'Simple Computer':
        black_player = MiniMaxPlayer(game, depth, 99, evaluate_score_by_piece)
    elif black_player == 'Complex Computer':
        black_player = MiniMaxPlayer(game, depth, 99, evaluate_score_by_position)
    else:
        black_player = 'HUMAN'

    run_game(game, black_player, white_player, player_info=info)


if __name__ == '__main__':
    # initialize the window
    window = tk.Tk()
    window.title('My Window')
    window.geometry('700x350')
    tk.Label(window, text='Reversi Game', font=('Arial', 16)).pack()
    frame = tk.Frame(window)
    frame.pack()
    vs_mode = tk.Frame(frame)
    analysis_mode = tk.Frame(frame)
    evaluation_mode = tk.Frame(frame)
    vs_mode.pack(side='left')
    analysis_mode.pack(side='left')
    evaluation_mode.pack(side='left')

    # UI for vs mode
    tk.Label(vs_mode, text='VS Mode', bg='green').pack()
    tk.Label(vs_mode, text='select black player').pack()
    menu1 = ttk.Combobox(vs_mode)
    menu1['value'] = ('Human', 'Random Computer', 'Simple Computer', 'Complex Computer')
    menu1.current(0)
    menu1.pack()
    tk.Label(vs_mode, text='select white player').pack()
    menu2 = ttk.Combobox(vs_mode)
    menu2['value'] = ('Human', 'Random Computer', 'Simple Computer', 'Complex Computer')
    menu2.current(3)
    menu2.pack()
    tk.Label(vs_mode, text='select the depth of the game tree'
                           '\nif computer player exist notice \n'
                           'depth 5 takes very long time').pack()
    menu3 = ttk.Combobox(vs_mode)
    menu3['value'] = ('1', '2', '3', '4', '5')
    menu3.current(2)
    menu3.pack()
    button1 = tk.Button(vs_mode, text='start game', width=15, height=2, command=start_game)
    button1.pack()

    # UI for analysis mode
    tk.Label(analysis_mode, text='Analysis Mode', bg='yellow').pack()
    button2 = tk.Button(analysis_mode,
                        text='start analysis',
                        width=15, height=2,
                        command=start_analysis)
    button2.pack()

    # UI for evaluation mode
    tk.Label(evaluation_mode, text='Evaluation Mode', bg='red').pack()
    tk.Label(evaluation_mode, text='Compare the performance score \n'
                                   'of simple computer player \n'
                                   'and complex computer player \n'
                                   'where score = (win+(tie/2))/n\n').pack()

    tk.Label(evaluation_mode, text='select the number of \n'
                                   'games for analysis').pack()
    menu4 = ttk.Combobox(evaluation_mode)
    menu4['value'] = (5, 10, 20, 50, 100)
    menu4.current(0)
    menu4.pack()
    tk.Label(evaluation_mode, text='select the depth of game tree\n'
                                   'Notice: depth 3, 4 takes \n'
                                   'very long time').pack()
    menu5 = ttk.Combobox(evaluation_mode)
    menu5['value'] = (1, 2, 3, 4)
    menu5.current(1)
    menu5.pack()
    button3 = tk.Button(evaluation_mode,
                        text='compare performance',
                        width=15, height=2,
                        command=compare_performance)
    button3.pack()
    window.mainloop()
