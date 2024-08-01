from arena import Strategy
from typing import Literal

import random


class RS_prob_bias(Strategy):
    name = "RS_prob_bias"
    author = "BohnerAdrian"

    def play(self) -> Literal["rock"] | Literal["paper"] | Literal["scissors"]:
        if random.random()<0.2:
            return random.choice(["paper", "scissors"])
        else:
            return random.choice(["rock", "scissors"])

    def handle_moves(
        self,
        own_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
        opponent_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
    ):
        pass


strategy = RS_prob_bias
