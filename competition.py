# competition.py
from arena import Arena
from util import import_strategies
import pandas as pd

class Competition:
    def __init__(self):
        self.result_vector = []

    def start_competition(self, selected_strategies):
        if 'All' in selected_strategies:
            strategies = import_strategies("strategies")
        else:
            strategies = [s for s in import_strategies("strategies") if s.name in selected_strategies]
        
        arena = Arena(strategies)
        result_df = arena.start()
        self.result_vector = arena.result_vector
        return result_df

    def get_strategy_matches(self, strategy_name):
        
        result_df = pd.DataFrame(self.result_vector, columns=[
            "GameNumber", "Strategy1", "Author1", "Strategy2", "Author2", "Startegy1_score", "Strategy2_score"
        ])
        matches = result_df[(result_df['Strategy1'] == strategy_name) | (result_df['Strategy2'] == strategy_name)]
        
        # Round the scores to 3 decimal places
        matches['Startegy1_score'] = matches['Startegy1_score'].round(3)
        matches['Strategy2_score'] = matches['Strategy2_score'].round(3)

        return matches.to_dict(orient='records')

