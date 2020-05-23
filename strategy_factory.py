from compare_all_moves_strategy import CompareAllMoves
from strategies import MoveFurthestBackStrategy, HumanStrategy, MoveRandomPiece


class StrategyFactory:
    @staticmethod
    def create_by_name(strategy_name):
        for strategy in StrategyFactory.get_all():
            if strategy.__name__ == strategy_name:
                return strategy()

        raise Exception("Cannot find strategy %s" % strategy_name)

    @staticmethod
    def get_all():
        strategies = [
            MoveRandomPiece,
            MoveFurthestBackStrategy,
            CompareAllMoves,
            HumanStrategy,
        ]
        return strategies
