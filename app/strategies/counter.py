from arena import Strategy
from typing import Literal

import random

class CounterStrategy(Strategy):
    
    name = "CounterStrategy"
    author = "BohnerAdrian"
    history = []
    
    def is_winner(self, own_move, opponent_move):
        if (
            (own_move == "rock" and opponent_move == "scissors") 
            or (own_move == "paper" and opponent_move == "rock")
            or (own_move == "scissors" and opponent_move == "paper")):
            return True
        else:
            return False
        
    def counter_move(self, move):
        if move == "rock":
            return "paper"
        elif move == "scissors":
            return "rock"
        else:
            return "scissors"

    def play(self) -> Literal["rock"] | Literal["paper"] | Literal["scissors"]:
        if not self.history:
            return random.choice(["rock", "paper", "scissors"])
        else:
            last_own_move = self.history[-1][0]
            last_opponent_move = self.history[-1][1]
            last_is_winning_move = self.is_winner(last_own_move, last_opponent_move)
            
            if last_is_winning_move:
                next_move = last_own_move
            else:
                next_move = self.counter_move(last_own_move)
                
            return next_move

    def handle_moves(
        self,
        own_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
        opponent_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
    ):
        self.history.append((own_move, opponent_move))
        
strategy = CounterStrategy

