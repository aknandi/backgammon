import multiprocessing as mp
import time

from colour import Colour
from game import Game


class Experiment:
    def __init__(self):
        self.__games_to_play = 1000
        self.__white_start_count = 0
        self.__white_win_count = 0
        self.__elapsed_time = 0

    def run(self):
        start_time = time.time()

        pool = mp.Pool(mp.cpu_count())
        result = pool.map(GamePlayer(), range(self.__games_to_play))
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
    def __init__(self):
        pass

    def __call__(self, src):
        game = Game()
        game.run_game(verbose=False)
        return game.who_started(), game.who_won()
