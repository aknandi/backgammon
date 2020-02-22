# Play backgammon

from experiment import Experiment
from game import Game
from strategies import MoveFurthestBackStrategy, MoveRandomPiece, CompareAllMoves

experiment = Experiment(
    games_to_play=1000,
    white_strategy=MoveFurthestBackStrategy(),
    black_strategy=CompareAllMoves()
)
if __name__ == '__main__':
    experiment.run()
    experiment.print_results()


# Null hypothesis is that the strategies equally good
# Define a joint event of a random coin toss to determine who starts followed by a game,
# Under the null hypothesis, for a single event, p(win) = 0.5
# Assuming the strategies are equal (null hypothesis): P(n_wins) = binom(n_wins, n_games, 0.5)
