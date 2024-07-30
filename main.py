from arena import Arena
from util import import_strategies

arena = Arena(import_strategies("strategies"))


arena.start()

scores = arena.scores

scores_sorted = sorted(scores.items(), key=lambda entry: entry[1], reverse=True)


longest_index = len(str(len(scores_sorted)))
longest_name = max(*[len(x[0]) for x in scores_sorted])
longest_score = max(*[len(str(x[1])) for x in scores_sorted])

line_length = 2 + longest_index + 2 + longest_name + 2 + longest_score + 2

print("#" + "-" * (line_length - 2) + "#")

for i, (name, score) in enumerate(scores_sorted):
    print(
        "| "
        + f"{i+1}. ".ljust(longest_index, " ")
        + str(name).ljust(longest_name, " ")
        + "  "
        + str(score).rjust(longest_score, " ")
        + " |"
    )

    if i + 1 < len(scores_sorted):
        print("|" + "-" * (line_length - 2) + "|")

print("#" + "-" * (line_length - 2) + "#")
