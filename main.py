# Play backgammon

from experiment import Experiment
from strategies import MoveFurthestBackStrategy, MoveRandomPiece

experiment = Experiment(
    games_to_play=1000,
    white_strategy=MoveFurthestBackStrategy(),
    black_strategy=MoveRandomPiece()
)
if __name__ == '__main__':
    experiment.run()
    experiment.print_results()
