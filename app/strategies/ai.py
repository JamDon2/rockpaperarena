from arena import Strategy
from typing import Literal
from tensorflow.keras.models import load_model
import numpy as np


class AIStrategy(Strategy):
    name = "AIStrategy"
    author = "JamDon2"

    def __init__(self) -> None:
        self.model = load_model("app/strategies/ai-models/model.keras")
        self.history = np.array([])
        self.option_to_tensor = {
            "rock": np.array([1, 0, 0]),
            "paper": np.array([0, 1, 0]),
            "scissors": np.array([0, 0, 1]),
        }
        self.options = ["rock", "paper", "scissors"]

    def play(self) -> Literal["rock"] | Literal["paper"] | Literal["scissors"]:
        input_slice = self.history[-600:]

        if len(input_slice) < 600:
            input_slice = np.pad(input_slice, (600 - len(input_slice), 0))

        prediction = self.model.predict(np.expand_dims(input_slice, axis=0), verbose=0)[
            0
        ]

        return self.options[np.argmax(prediction)]

    def handle_moves(
        self,
        own_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
        opponent_move: Literal["rock"] | Literal["paper"] | Literal["scissors"],
    ):
        self.history = np.append(
            self.history,
            np.concatenate(
                [self.option_to_tensor[own_move], self.option_to_tensor[opponent_move]]
            ),
        )


strategy = AIStrategy
