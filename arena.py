# arena.py
from abc import ABC, abstractmethod
from typing import Literal, Type
from scorers import Scorer
import pandas as pd
from flask_sse import sse

OPTIONS = Literal["rock", "paper", "scissors"]
ROUNDS = 20
GAMES = 20
NO_POINT_THRESHOLD = 0.001
POINTS_PER_GAME = 10

class Strategy(ABC):
    name: str
    author: str

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
    def __init__(self, strategies: list[Type[Strategy]], rounds, games, points_per_game, max_point_threshold=0.8, scorer_type="Simple") -> None:
        self.strategies = strategies
        self.scores = {}
        self.result_vector = []
        self.rounds = rounds
        self.games = games
        self.max_points_per_game = points_per_game
        self.max_point_threshold = max_point_threshold
        self.scorer_type = scorer_type

    def start(self) -> pd.DataFrame:
        total_matches = self.games * (len(self.strategies) * (len(self.strategies) - 1)) // 2
        match_count = 0

        for i in range(self.games):
            for strategy1_id, strategy1 in enumerate(self.strategies):
                for strategy2 in self.strategies[strategy1_id + 1:]:
                    match_count += 1
                    game = Game(strategy1(), strategy2())

                    wins1, wins2, ties = game.play_rounds(n=self.rounds)

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

                    # Assume Scorer class is defined elsewhere and imported
                    if self.scorer_type == "Simple":
                        scorer = Scorer(wins1, wins2, ties, self.max_points_per_game, self.max_point_threshold)

                    first_score, second_score = scorer.simple_scorer()

                    result = [i + 1, strategy1.name, strategy1.author, strategy2.name, strategy2.author, first_score, second_score]

                    self.result_vector.append(result)

                    self.scores[strategy1.name] += first_score
                    self.scores[strategy2.name] += second_score

                    # Send progress update
                    print(f"Publishing progress: {match_count / total_matches * 100}%")
                    sse.publish({"progress": match_count / total_matches * 100}, type='progress')

        result_df = pd.DataFrame(self.result_vector, columns=["GameNumber", "Strategy1", "Author1", "Strategy2", "Author2", "Strategy1_score", "Strategy2_score"])

        result_df["Strategy1_score"] = result_df["Strategy1_score"].round(3)
        result_df["Strategy2_score"] = result_df["Strategy2_score"].round(3)

        # Send completion message
        print("Publishing completion message")
        sse.publish({"status": "complete"}, type='progress')

        return result_df
