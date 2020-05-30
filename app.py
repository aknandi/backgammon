from flask import Flask

from src.board import Board

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start-game')
def start_game():
    board = Board.create_starting_board()
    return board.to_json()

