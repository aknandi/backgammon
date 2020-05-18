import multiprocessing as mp
import time
from random import randint

from colour import Colour
from game import Game, Strategy
from scipy.stats import binom


class Experiment:
    def __init__(self, games_to_play: int, white_strategy: Strategy, black_strategy: Strategy, parallelise: bool = True):
        self.__games_to_play = games_to_play
        self.__results = []
        self.__elapsed_time = 0
        self.__white_strategy = white_strategy
        self.__black_strategy = black_strategy
        self.__parallelise = parallelise

    def run(self):
        start_time = time.time()

        player = GamePlayer(self.__white_strategy, self.__black_strategy)
        index_range = range(self.__games_to_play)

        if self.__parallelise:
            pool = mp.Pool(mp.cpu_count())
            self.__results = pool.map(player, index_range)
            pool.close()
        else:
            self.__results = [player.__call__(i) for i in index_range]

        self.__elapsed_time = time.time() - start_time

    def print_results(self):
        white_start_count = sum(1 for x in self.__results if x[0] == Colour.WHITE)
        white_win_count = self.get_white_wins()

        if white_win_count < 0.5 * self.__games_to_play:
            probability = 2 * binom.cdf(white_win_count, self.__games_to_play, 0.5)
        else:
            probability = 2 * binom.cdf(self.__games_to_play - white_win_count, self.__games_to_play, 0.5)

        print("After %d games" % self.__games_to_play)
        print("White starts: %d" % white_start_count)
        print("White wins: %d" % white_win_count)
        print("Time taken: %.2f s" % self.__elapsed_time)
        print("Assuming the strategies are equally as good,",
              "the probability of this discrepancy in wins is %.8f" % probability)

    def get_white_wins(self):
        return sum(1 for x in self.__results if x[1] == Colour.WHITE)


class GamePlayer:
    def __init__(self, white_strategy, black_strategy):
        self.__white_strategy = white_strategy
        self.__black_strategy = black_strategy

    def __call__(self, game_index):
        print(".", end="")
        game = Game(
            white_strategy=self.__white_strategy,
            black_strategy=self.__black_strategy,
            first_player=Colour(randint(0, 1))
        )
        game.run_game(verbose=False)
        return game.who_started(), game.who_won()
