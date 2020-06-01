from flask import Flask, request
from flask_cors import CORS, cross_origin
from src.board import Board

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
board = Board.create_starting_board()

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start-game')
@cross_origin()
def start_game():
    return board.to_json()


@app.route('/move-piece')
@cross_origin()
def move_piece():
    location = request.args.get('location', default=1, type=int)
    die_roll = request.args.get('die-roll', default=1, type=int)
    board.move_piece(board.get_piece_at(location), die_roll)
    return board.to_json()
