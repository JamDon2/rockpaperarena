
class Scorer:
    
    def __init__(self, wins1, wins2, ties, max_points_per_game, max_point_threshold):
        self.wins1 = wins1
        self.wins2 = wins2
        self.ties = ties
        self.max_points_per_game = max_points_per_game
        self.max_points_threshold = max_point_threshold
        
        
    def simple_scorer(self):
        first_strategy_score = round(self.max_points_per_game * self.wins1 / (self.wins1 + self.wins2), 3)
        second_strategy_score = round(self.max_points_per_game - first_strategy_score, 3)
        
        return first_strategy_score, second_strategy_score
    
    def advanced_scorer(self):
        first_strategy_score = max(min((self.wins1 / (self.wins1 + self.wins2) - 0.5) / (self.max_points_threshold - 0.5), 1),-1) * self.max_points_per_game
        second_strategy_score = max(min((self.wins2 / (self.wins1 + self.wins2) - 0.5) / (self.max_points_threshold - 0.5), 1),-1) * self.max_points_per_game
        
        return first_strategy_score, second_strategy_score
