import multiprocessing as mp
import time

from colour import Colour
from game import Game, Strategy


class Experiment:
    def __init__(self, games_to_play: int, white_strategy: Strategy, black_strategy: Strategy):
        self.__games_to_play = games_to_play
        self.__white_start_count = 0
        self.__white_win_count = 0
        self.__elapsed_time = 0
        self.__white_strategy = white_strategy
        self.__black_strategy = black_strategy

    def run(self):
        start_time = time.time()

        pool = mp.Pool(mp.cpu_count())
        result = pool.map(GamePlayer(self.__white_strategy, self.__black_strategy), range(self.__games_to_play))
        pool.close()

        self.__white_start_count = sum(1 for x in result if x[0] == Colour.WHITE)
        self.__white_win_count = sum(1 for x in result if x[1] == Colour.WHITE)
        self.__elapsed_time = time.time() - start_time

    def print_results(self):
        print("After %d games" % self.__games_to_play)
        print("White starts: %d" % self.__white_start_count)
        print("White wins: %d" % self.__white_win_count)
        print("Time taken: %.2f s" % self.__elapsed_time)


class GamePlayer:
    def __init__(self, white_strategy, black_strategy):
        self.__white_strategy = white_strategy
        self.__black_strategy = black_strategy

    def __call__(self, src):
        game = Game(self.__white_strategy, self.__black_strategy)
        game.run_game(verbose=False)
        return game.who_started(), game.who_won()
