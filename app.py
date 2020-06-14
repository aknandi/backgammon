import queue
import threading
import time

from flask import Flask, request
from flask_cors import CORS, cross_origin

from src.board import Board
from src.colour import Colour
from src.compare_all_moves_strategy import CompareAllMovesSimple, CompareAllMovesWeightingDistanceAndSingles
from src.strategies import MoveRandomPiece, MoveFurthestBackStrategy
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


def game_thread(difficulty):
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

            print('[Game]: Sending opponents activity (end of previous turn, start of new turn)')
            move_results.put({
                'result': 'success',
                'opponents_activity': {
                    'opponents_move': [map_move(move) for move in opponents_activity['opponents_move']],
                    'dice_roll': opponents_activity['dice_roll'],
                },
                'board_after_your_last_turn': board_json_before_opp_move,
            })
            while len(dice_roll) > 0:
                print('[Game]: Waiting for moves_to_make...')
                move = moves_to_make.get()
                if move == 'end_game':
                    print('[Game]: ...got end_game, so crashing')
                    raise Exception("Game ended")
                elif move == 'end_turn':
                    print('[Game]: ...got end_turn')
                    break
                print('[Game]: ...got move')
                try:
                    rolls_moved = make_move(move['location'], move['die_roll'])
                    for roll in rolls_moved:
                        dice_roll.remove(roll)
                        used_die_rolls[0].append(roll)

                    if len(dice_roll) > 0:
                        print('[Game]: Sending move success (middle of go)')
                        move_results.put({
                            'result': 'success'
                        })
                except:
                    print('[Game]: Sending move failed')
                    move_results.put({
                        'result': 'move_failed'
                    })

            self.board_after_your_last_turn = board.create_copy()
            print('[Game]: Done last move of turn. Going to wait for opponent information')

        def game_over(self, opponents_activity):
            board_json_before_opp_move = self.board_after_your_last_turn.to_json()

            def map_move(move):
                self.board_after_your_last_turn.move_piece(
                    self.board_after_your_last_turn.get_piece_at(move['start_location']),
                    move['die_roll']
                )
                move['board_after_move'] = self.board_after_your_last_turn.to_json()
                return move

            print('[Game]: Sending opponents activity (end of game)')
            move_results.put({
                'result': 'success',
                'opponents_activity': {
                    'opponents_move': [map_move(move) for move in opponents_activity['opponents_move']],
                    'dice_roll': opponents_activity['dice_roll'],
                },
                'board_after_your_last_turn': board_json_before_opp_move,
            })

    print(difficulty)
    if difficulty == 'easy':
        opponent_strategy = MoveRandomPiece()
    elif difficulty == 'medium':
        opponent_strategy = MoveFurthestBackStrategy()
    elif difficulty == 'hard':
        opponent_strategy = CompareAllMovesSimple()
    elif difficulty == 'veryhard':
        opponent_strategy = CompareAllMovesWeightingDistanceAndSingles()
    else:
        raise Exception('Not a valid strategy')

    print('[Game]: Starting game with strategy %s' % opponent_strategy.__class__.__name__)

    game = Game(
        white_strategy=ApiStrategy(),
        black_strategy=opponent_strategy,
        first_player=Colour(randint(0, 1))
    )
    current_board.append(game.board)
    game.run_game(verbose=False)

    # Thread is only ended by an 'end_game' move
    while True:
        print('[Game]: run_game has completed, waiting for moves_to_make...')
        if moves_to_make.get() == 'end_game':
            print('[Game] ... got end_game (in final bit)')
            break
        else:
            print('[Game] ... got non-end_game (in final bit)')
            move_results.put({
                        'result': 'move_failed'
                    })


def get_state(response={}):
    if len(current_board) == 0:
        return {'board': "{}", 'dice_roll': [], 'used_rolls': []}
    board = current_board[0]
    move = current_roll[0]
    moves_left = move.copy()
    for used_move in used_die_rolls[0]:
        moves_left.remove(used_move)

    state = {'board': board.to_json(),
             'dice_roll': move,
             'used_rolls': used_die_rolls[0],
             'player_can_move': not board.no_moves_possible(Colour.WHITE, moves_left)}
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


@app.route('/start-game')
@cross_origin()
def start_game():
    return get_state()


@app.route('/move-piece')
@cross_origin()
def move_piece():
    print('[API]: move-piece called')
    location = request.args.get('location', default=1, type=int)
    die_roll = request.args.get('die-roll', default=1, type=int)
    end_turn = request.args.get('end-turn', default='', type=str)
    print(end_turn)
    if end_turn == 'true':
        print('[API]: Sending end_turn...')
        moves_to_make.put('end_turn')
    else:
        print('[API]: Sending moves_to_make...')
        moves_to_make.put({
            'location': location,
            'die_roll': die_roll
        })
    print('[API]: Waiting for move_results...')
    response = move_results.get()
    print('[API]: ...got result, responding to frontend')
    return get_state(response)


@app.route('/new-game')
@cross_origin()
def new_game():
    difficulty = request.args.get('difficulty', default='hard', type=str)
    print(difficulty)
    print('[API]: new-game called')
    if len(current_board) != 0:
        print('[API]: Sending end_game')
        moves_to_make.put('end_game')
    current_board.clear()
    current_roll.clear()
    time.sleep(1)
    print('[API]: Starting new game thread')
    threading.Thread(target=game_thread, args=[difficulty]).start()
    print('[API]: Waiting for move_results...')
    response = move_results.get()
    print('[API]: ...got result, responding to frontend')
    return get_state(response)
