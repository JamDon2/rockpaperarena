from arena import Strategy
from typing import Literal
from tensorflow.lite.python.interpreter import Interpreter
import numpy as np


class FastAI500Strategy(Strategy):
    name = "FastAI500Strategy"
    author = "JamDon2"

    def __init__(self) -> None:
        self.interpeter = Interpreter("model-500.tflite")
        self.runner = self.interpeter.get_signature_runner("serving_default")
        self.history = np.array([])
        self.option_to_tensor = {
            "rock": np.array([1, 0, 0]),
            "paper": np.array([0, 1, 0]),
            "scissors": np.array([0, 0, 1]),
        }
        self.options = ["rock", "paper", "scissors"]

    def play(self) -> Literal["rock"] | Literal["paper"] | Literal["scissors"]:
        input_slice = self.history[-3000:]

        if len(input_slice) < 3000:
            input_slice = np.pad(input_slice, (3000 - len(input_slice), 0))

        prediction = self.runner(keras_tensor=input_slice.astype("float32"))[
            "output_0"
        ][0]

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


strategy = FastAI500Strategy