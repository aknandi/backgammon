# Play backgammon
from src.compare_all_moves_strategy import CompareAllMoves6, CompareAllMoves7
from src.experiment import Experiment

experiment = Experiment(
    games_to_play=200,
    white_strategy=CompareAllMoves6(),
    black_strategy=CompareAllMoves7()
)
if __name__ == '__main__':
    experiment.run()
    experiment.print_results()


# Null hypothesis is that the strategies equally good
# Define a joint event of a random coin toss to determine who starts followed by a game,
# Under the null hypothesis, for a single event, p(win) = 0.5
# Assuming the strategies are equal (null hypothesis): P(n_wins) = binom(n_wins, n_games, 0.5)
