from arena import Strategy
from typing import Literal

import random


class RandomStrategy_biased(Strategy):
    
    name = "RandomStrategy_biased"
    author = "BohnerAdrian"

    def play(self) -> Literal["rock"] | Literal["paper"] | Literal["scissors"]:
        return random.choice(["rock", "paper", "scissors", "rock", "rock"])

    def handle_moves(
        self,
        own_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
        opponent_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
    ):
        pass
    

strategy = RandomStrategy_biased

