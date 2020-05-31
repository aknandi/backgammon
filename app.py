from flask import Flask
from flask_cors import CORS, cross_origin
from src.board import Board

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start-game')
@cross_origin()
def start_game():
    board = Board.create_starting_board()
    return board.to_json()


