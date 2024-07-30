from arena import Strategy
from typing import Literal

import random


class RandomStrategy(Strategy):
    name = "RandomStrategy"

    def play(self) -> Literal["rock"] | Literal["paper"] | Literal["scissors"]:
        return random.choice(["rock", "paper", "scissors"])

    def handle_moves(
        self,
        own_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
        opponent_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
    ):
        pass


strategy = RandomStrategy
