import multiprocessing as mp
import time

from colour import Colour
from game import Game, Strategy
from scipy.stats import binom


class Experiment:
    def __init__(self, games_to_play: int, white_strategy: Strategy, black_strategy: Strategy):
        self.__games_to_play = games_to_play
        self.__white_start_count = 0
        self.__white_win_count = 0
        self.__elapsed_time = 0
        self.__white_strategy = white_strategy
        self.__black_strategy = black_strategy
        self.__probability = 0

    def run(self):
        start_time = time.time()

        pool = mp.Pool(mp.cpu_count())
        result = pool.map(GamePlayer(self.__white_strategy, self.__black_strategy), range(self.__games_to_play))
        pool.close()

        self.__white_start_count = sum(1 for x in result if x[0] == Colour.WHITE)
        self.__white_win_count = sum(1 for x in result if x[1] == Colour.WHITE)
        self.__elapsed_time = time.time() - start_time

        if self.__white_win_count < 0.5 * self.__games_to_play:
            self.__probability = 2 * binom.cdf(self.__white_win_count, self.__games_to_play, 0.5)
        else:
            self.__probability = 2 * binom.cdf(self.__games_to_play - self.__white_win_count, self.__games_to_play, 0.5)

    def print_results(self):
        print("After %d games" % self.__games_to_play)
        print("White starts: %d" % self.__white_start_count)
        print("White wins: %d" % self.__white_win_count)
        print("Time taken: %.2f s" % self.__elapsed_time)
        print("Assuming the strategies are equally as good, ",
              "the probability of this discrepancy in wins is %.8f" % self.__probability)


class GamePlayer:
    def __init__(self, white_strategy, black_strategy):
        self.__white_strategy = white_strategy
        self.__black_strategy = black_strategy

    def __call__(self, src):
        game = Game(self.__white_strategy, self.__black_strategy)
        game.run_game(verbose=False)
        return game.who_started(), game.who_won()
