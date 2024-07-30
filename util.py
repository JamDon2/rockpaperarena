import os
import importlib.util
from arena import Strategy
from typing import Type


def import_strategies(directory: str) -> list[Type[Strategy]]:
    strategy_files = os.listdir(directory)

    strategies = []

    for file in strategy_files:
        if not file.endswith(".py") or file.endswith(".wip.py"):
            continue

        spec = importlib.util.spec_from_file_location(
            "strategy", os.path.join(directory, file)
        )

        strategy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(strategy_module)

        strategy: Type[Strategy] = strategy_module.strategy

        strategies.append(strategy)

    return strategies
