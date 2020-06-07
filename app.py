import queue
import threading
import time

from flask import Flask, request
from flask_cors import CORS, cross_origin
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
current_move = []


def game_thread():
    class ApiStrategy(Strategy):
        def move(self, board, colour, dice_roll, make_move):
            current_move.insert(0, dice_roll)
            while len(dice_roll) > 0 and not board.no_moves_possible(colour, dice_roll):
                move = moves_to_make.get()
                if move == 'end_game':
                    raise Exception()
                try:
                    rolls_moved = make_move(move['location'], move['die_roll'])
                    for roll in rolls_moved:
                        dice_roll.remove(roll)
                    move_results.put("done")
                except:
                    move_results.put("fail")

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


threading.Thread(target=game_thread).start()


def get_state(board, move):
    state = {'board': board.to_json(),
             'dice_roll': move}
    if board.has_game_ended():
        state['winner'] = str(board.who_won())
    return state


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start-game')
@cross_origin()
def start_game():
    return get_state(current_board[0], current_move[0])


@app.route('/move-piece')
@cross_origin()
def move_piece():
    location = request.args.get('location', default=1, type=int)
    die_roll = request.args.get('die-roll', default=1, type=int)
    moves_to_make.put({
        'location': location,
        'die_roll': die_roll
    })
    move_results.get()
    time.sleep(0.2)
    return get_state(current_board[0], current_move[0])


@app.route('/new-game')
@cross_origin()
def new_game():
    moves_to_make.put('end_game')
    current_board.clear()
    current_move.clear()
    threading.Thread(target=game_thread).start()
    time.sleep(0.1)
    return get_state(current_board[0], current_move[0])


