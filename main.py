from arena import Arena
from util import import_strategies
import pandas as pd
from tabulate import tabulate

arena = Arena(import_strategies("strategies"))


result_df = arena.start()

strategy_scores = pd.concat([
    result_df[['Strategy1', 'Author1', 'Startegy1_score']].rename(columns={'Strategy1': 'Strategy', 'Author1': 'Author', 'Startegy1_score': 'Score'}),
    result_df[['Strategy2', 'Author2', 'Strategy2_score']].rename(columns={'Strategy2': 'Strategy', 'Author2': 'Author', 'Strategy2_score': 'Score'})
])

# Group by the strategy and sum the scores
strategy_total_scores = strategy_scores.groupby(['Strategy', 'Author'])['Score'].sum().reset_index().sort_values('Score', ascending = False)
