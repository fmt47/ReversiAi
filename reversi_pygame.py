"""CSC111 Final Project: AI Player for Reversi

Instructions:
This Python module contains the pygame application which allows
human vs human, haman vs computer, and computer vs computer

Copyright and Usage Information:
This file is Copyright (c) 2021 Yupeng Chang, Huiru Tan, Xi Chen.
"""
import pygame
from reversi_board import Reversi, BLACK_PIECE, WHITE_PIECE, EMPTY_PIECE
from reversi_player import RandomPlayer, Player, \
    evaluate_score_by_piece, generate_game_tree, apply_minimax
from pygame.colordict import THECOLORS
from typing import Union
from time import sleep, time

SCREEN_SIZE = (960, 800)  # (width, height)
UNIT = 80
GRID_SIDE = 60


def initialize_screen(screen_size: tuple[int, int], allowed: list) -> pygame.Surface:
    """Initialize pygame and the display window.
    allowed is a list of pygame event types that should be listened for while pygame is running.
    This is code modified from assignment 1
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS['white'])
    pygame.display.flip()
    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def draw_ui(screen: pygame.Surface) -> None:
    """Draw the board and the user interface
    """
    color = THECOLORS['black']
    width, height = screen.get_size()

    for col in range(1, 12):
        x = col * (width // 12)
        pygame.draw.line(screen, color, (x, 0), (x, height))

    for row in range(1, 10):
        y = row * (height // 10)
        pygame.draw.line(screen, color, (0, y), (width, y))

    pygame.draw.rect(screen, THECOLORS['gray10'],
                     pygame.Rect(0, 0, UNIT, 9 * UNIT), 0)
    pygame.draw.rect(screen, THECOLORS['gray10'],
                     pygame.Rect(0, 0, 11 * UNIT, UNIT), 0)
    pygame.draw.rect(screen, THECOLORS['gray10'],
                     pygame.Rect(0, 9 * UNIT, 11 * UNIT, UNIT), 0)
    pygame.draw.rect(screen, THECOLORS['gray10'],
                     pygame.Rect(9 * UNIT, 0, 3 * UNIT, 10 * UNIT), 0)

    for x in range(8):
        draw_text(screen, str(x), 1.4 * UNIT + x * UNIT, 0.7 * UNIT)
        draw_text(screen, str(x), 0.7 * UNIT, 1.4 * UNIT + x * UNIT)


def draw_score(screen: pygame.Surface, row: int, column: int, score: int) -> None:
    """show score on (row, column) of the board"""
    draw_text(screen, str(score), (1.5 + column) * UNIT - 5, (1.5 + row) * UNIT - 5)


def draw_piece(screen: pygame.Surface, row: int, column: int, piece: any) -> None:
    """place pieces on board"""
    color = THECOLORS['black'] if piece == BLACK_PIECE else THECOLORS['white']
    pygame.draw.circle(screen, color, ((1.5 + column) * UNIT, (1.5 + row) * UNIT), 25)


def update_ui(screen: pygame.Surface, game: Reversi):
    """update the user interface"""
    board = game.board
    next_player = 'black' if game.is_black_move else 'white'
    for row in range(8):
        for column in range(8):
            piece = board[row][column]
            if piece != EMPTY_PIECE:
                draw_piece(screen, row, column, piece)
    draw_text(screen, f'current player is: {next_player}', 9.2 * UNIT, UNIT)
    draw_text(screen, f'black score: {game.black_score}', 9.2 * UNIT, 1.5 * UNIT)
    draw_text(screen, f'white score: {game.white_score}', 9.2 * UNIT, 2 * UNIT)
    draw_text(screen, f'To exit the game', 9.2 * UNIT, 8 * UNIT)
    draw_text(screen, f'Stop the main program', 9.2 * UNIT, 8.5 * UNIT)

    winner = game.winner()
    if winner is not None:
        draw_text(screen, f'GAME END', 9.2 * UNIT, 4 * UNIT)
        draw_text(screen, f'WINNER IS: {winner}', 9.2 * UNIT, 4.5 * UNIT)


def draw_player_info(screen: pygame.Surface,
                     black_player: str,
                     white_player: str,
                     depth: int) -> None:
    """print the players name"""
    if black_player in {'HUMAN', 'Random Computer'} and white_player in {'HUMAN',
                                                                         'Random Computer'}:
        depth = 'N/A'
    draw_text(screen, f'black player: {black_player}', 9.2 * UNIT, 3 * UNIT)
    draw_text(screen, f'white player: {white_player}', 9.2 * UNIT, 3.5 * UNIT)
    draw_text(screen, f'game tree depth: {depth}', 9.2 * UNIT, 4 * UNIT)


def draw_text(screen: pygame.Surface, text: str, left, top) -> None:
    """Draw the given text to the pygame screen at the given position.
    Modified from a1.
    """
    font = pygame.font.SysFont('inconsolata', 22)
    text_surface = font.render(text, True, THECOLORS['gray'])
    width, height = text_surface.get_size()
    screen.blit(text_surface,
                pygame.Rect((left, top), (left + width, top + height)))


def human_move(event: pygame.event.Event) -> tuple:
    """player make move"""
    column = (event.pos[0] - UNIT) // UNIT
    row = (event.pos[1] - UNIT) // UNIT
    return row, column


def run_game(game: Reversi,
             black_player: Union[str, Player],
             white_player: Union[str, Player],
             time_interval: float = 1,
             player_info=None) -> None:
    """Main method for the game
    player is either 'HUMAN' or a player object"""
    screen = initialize_screen(SCREEN_SIZE, [pygame.MOUSEBUTTONDOWN])

    while True:
        screen.fill(THECOLORS['darkgreen'])
        draw_ui(screen)
        update_ui(screen, game)
        if player_info is not None:
            draw_player_info(screen, player_info[0], player_info[1], player_info[2])
        pygame.display.flip()  # update the screen

        if game.winner() is None:
            if game.is_black_move:
                if black_player == 'HUMAN':
                    event = pygame.event.wait()
                    new_move = human_move(event)
                else:
                    new_move = black_player.think_move()
                    sleep(time_interval)  # time interval between human move and computer move

            else:
                if white_player == 'HUMAN':
                    event = pygame.event.wait()
                    new_move = human_move(event)
                else:
                    new_move = white_player.think_move()
                    sleep(time_interval)  # time interval between human move and computer move

            if new_move in game.valid_moves:
                game.make_move(new_move)

                # show the last move
                piece = WHITE_PIECE if game.is_black_move else BLACK_PIECE
                draw_piece(screen, new_move[0], new_move[1], piece)
                pygame.display.flip()
                sleep(0.5)

        else:
            pygame.event.wait()


def analysis_game(game: Reversi) -> None:
    """Main method for the analysis mode, show the score of each possible move"""
    screen = initialize_screen(SCREEN_SIZE, [pygame.MOUSEBUTTONDOWN])

    while True:
        screen.fill(THECOLORS['darkgreen'])
        draw_ui(screen)
        update_ui(screen, game)
        start_time = time()
        game_tree = generate_game_tree('*', game, 3, start_time, 99,
                                       game.is_black_move, evaluate_score_by_piece)
        apply_minimax(game_tree, game.is_black_move)
        for s in game_tree.sub_trees:
            draw_score(screen, s.move[0], s.move[1], s.score)

        pygame.display.flip()  # update the screen

        event = pygame.event.wait()
        new_move = human_move(event)

        if new_move in game.valid_moves:
            game.make_move(new_move)

            # show the last move
            piece = WHITE_PIECE if game.is_black_move else BLACK_PIECE
            draw_piece(screen, new_move[0], new_move[1], piece)
            pygame.display.flip()
            sleep(0.5)


if __name__ == '__main__':
    # human vs random computer
    reversi_game = Reversi()
    random_player = RandomPlayer(reversi_game)
    run_game(reversi_game, 'HUMAN', random_player)
