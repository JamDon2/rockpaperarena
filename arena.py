from abc import ABC, abstractmethod
from typing import Literal, Type


OPTIONS = Literal["rock", "paper", "scissors"]
ROUNDS = 2000
GAMES = 10
NO_POINT_THRESHOLD = 0.05
POINTS_PER_GAME = 10


class Strategy(ABC):
    name: str

    @abstractmethod
    def play(self) -> OPTIONS:
        pass

    @abstractmethod
    def handle_moves(self, own_move: OPTIONS, opponent_move: OPTIONS):
        pass


class Game:
    def __init__(self, strategy1: Strategy, strategy2: Strategy) -> None:
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.win1 = 0
        self.win2 = 0
        self.tie = 0

    def _play(self) -> None:
        choice1 = self.strategy1.play()
        choice2 = self.strategy2.play()

        self.strategy1.handle_moves(choice1, choice2)
        self.strategy2.handle_moves(choice2, choice1)

        if choice1 == choice2:
            self.tie += 1
        elif (
            (choice1 == "rock" and choice2 == "scissors")
            or (choice1 == "paper" and choice2 == "rock")
            or (choice1 == "scissors" and choice2 == "paper")
        ):
            self.win1 += 1
        else:
            self.win2 += 1

    def play_rounds(self, n=ROUNDS) -> tuple[int, int, int]:
        for i in range(n):
            self._play()

        return self.win1, self.win2, self.tie


class Arena:
    def __init__(self, strategies: list[Type[Strategy]]) -> None:
        self.strategies = strategies
        self.scores = {}

    def start(self) -> None:
        for i in range(GAMES):
            for strategy1_id, strategy1 in enumerate(self.strategies):
                for strategy2 in self.strategies[:strategy1_id]:
                    game = Game(strategy1(), strategy2())

                    wins1, wins2, ties = game.play_rounds()

                    if strategy1.name not in self.scores:
                        self.scores[strategy1.name] = 0

                    if strategy2.name not in self.scores:
                        self.scores[strategy2.name] = 0

                    if (
                        wins1 + wins2 < ties
                        or abs(wins1 - wins2)
                        < (wins1 + wins2 + ties) * NO_POINT_THRESHOLD
                    ):
                        continue

                    first_score = round(POINTS_PER_GAME * wins1 / (wins1 + wins2))

                    self.scores[strategy1.name] += first_score

                    self.scores[strategy2.name] += POINTS_PER_GAME - first_score
