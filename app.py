import queue
import threading
import time

from flask import Flask, request
from flask_cors import CORS, cross_origin

from src.board import Board
from src.colour import Colour
from src.compare_all_moves_strategy import CompareAllMovesWeightingDistanceAndSingles
from src.game import Game
from random import randint
from src.strategies import Strategy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

moves_to_make = queue.Queue()
move_results = queue.Queue()
current_board = []
current_roll = []
used_die_rolls = []


def set_current_move(dice_roll):
    current_roll.insert(0, dice_roll)
    del current_roll[1:]
    used_die_rolls.insert(0, [])
    del used_die_rolls[1:]


def game_thread():
    class ApiStrategy(Strategy):

        def __init__(self) -> None:
            self.board_after_your_last_turn = Board.create_starting_board()

        def move(self, board, colour, dice_roll, make_move, opponents_activity):
            set_current_move(dice_roll.copy())

            board_json_before_opp_move = self.board_after_your_last_turn.to_json()

            def map_move(move):
                self.board_after_your_last_turn.move_piece(
                    self.board_after_your_last_turn.get_piece_at(move['start_location']),
                    move['die_roll']
                )
                move['board_after_move'] = self.board_after_your_last_turn.to_json()
                return move

            move_results.put({
                'result': 'success',
                'opponents_activity': {
                    'opponents_move': [map_move(move) for move in opponents_activity['opponents_move']],
                    'dice_roll': opponents_activity['dice_roll'],
                },
                'board_after_your_last_turn': board_json_before_opp_move,
            })
            while len(dice_roll) > 0 and not board.no_moves_possible(colour, dice_roll):
                move = moves_to_make.get()
                if move == 'end_game':
                    raise Exception("Game ended")
                try:
                    rolls_moved = make_move(move['location'], move['die_roll'])
                    for roll in rolls_moved:
                        dice_roll.remove(roll)
                        used_die_rolls[0].append(roll)

                    if len(dice_roll) > 0 and not board.no_moves_possible(colour, dice_roll):
                        move_results.put({
                            'result': 'success'
                        })
                    else:
                        self.board_after_your_last_turn = board.create_copy()
                except:
                    move_results.put({
                        'result': 'move_failed'
                    })

    game = Game(
        white_strategy=ApiStrategy(),
        black_strategy=CompareAllMovesWeightingDistanceAndSingles(),
        first_player=Colour(randint(0, 1))
    )
    current_board.append(game.board)
    game.run_game()

    # Thread is only ended by an 'end_game' move
    while True:
        if moves_to_make.get() == 'end_game':
            break
        else:
            move_results.put("fail")


def get_state(response={}):
    if len(current_board) == 0:
        return {'board': "{}", 'dice_roll': [], 'used_rolls': []}
    board = current_board[0]
    move = current_roll[0]

    state = {'board': board.to_json(),
             'dice_roll': move,
             'used_rolls': used_die_rolls[0]}
    if board.has_game_ended():
        state['winner'] = str(board.who_won())
    if 'opponents_activity' in response:
        # dict, keys: start_location, die_roll, end_location
        opponents_activity = response['opponents_activity']
        state['opp_move'] = opponents_activity['opponents_move']
        state['opp_roll'] = opponents_activity['dice_roll']
    if 'board_after_your_last_turn' in response:
        state['board_after_your_last_turn'] = response['board_after_your_last_turn']
    if 'result' in response:
        state['result'] = response['result']
    return state


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start-game')
@cross_origin()
def start_game():
    return get_state()


@app.route('/move-piece')
@cross_origin()
def move_piece():
    location = request.args.get('location', default=1, type=int)
    die_roll = request.args.get('die-roll', default=1, type=int)
    moves_to_make.put({
        'location': location,
        'die_roll': die_roll
    })
    response = move_results.get()
    return get_state(response)


@app.route('/new-game')
@cross_origin()
def new_game():
    if len(current_board) != 0:
        moves_to_make.put('end_game')
    current_board.clear()
    current_roll.clear()
    threading.Thread(target=game_thread).start()
    response = move_results.get()
    return get_state(response)
