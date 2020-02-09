# Play backgammon

from experiment import Experiment
from strategies import MoveFurthestBackStrategy, MoveRandomPiece

experiment = Experiment(
    white_strategy=MoveFurthestBackStrategy(),
    black_strategy=MoveRandomPiece()
)
experiment.run()
experiment.print_results()
