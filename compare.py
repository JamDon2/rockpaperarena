from arena import Game
from util import import_strategies

ROUNDS = 10000

strategies = import_strategies("strategies")


for i, strategy in enumerate(strategies):
    print(f"{i+1}. {strategy.name}")

first = int(input("\nWhich is your first strategy? ")) - 1
second = (
    int(
        input(
            f"\nWhich strategy would you like to compare {strategies[first].name} against? "
        )
    )
    - 1
)

strategy1 = strategies[first]
strategy2 = strategies[second]

game = Game(strategy1(), strategy2())

win1, win2, tie = game.play_rounds(ROUNDS)

print(
    f"\n{strategy1.name} won {win1/ROUNDS:.2%} of rounds, it lost {win2/ROUNDS:.2%}, and tied on {tie/ROUNDS:.2%}."
)
