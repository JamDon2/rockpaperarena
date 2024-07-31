from arena import Strategy
from typing import Literal

import random


class Predictive(Strategy):
    
    name = "PredictiveStrategy"
    author = "BohnerAdrian"
    history = []

    def play(self) -> Literal["rock"] | Literal["paper"] | Literal["scissors"]:
        if not self.history:
            return random.choice(["rock", "paper", "scissors"])
        opponent_moves = [move[1] for move in self.history]
        if opponent_moves.count("rock") > opponent_moves.count("paper") and opponent_moves.count("rock") > opponent_moves.count("scissors"):
            return "paper"
        elif opponent_moves.count("paper") > opponent_moves.count("scissors"):
            return "scissors"
        else:
            return "rock"

    def handle_moves(
        self,
        own_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
        opponent_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
    ):
        self.history.append((own_move, opponent_move))
        
strategy = Predictive

