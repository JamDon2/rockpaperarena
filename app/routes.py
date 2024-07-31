from flask import Blueprint, render_template, request
from arena import Arena
from util import import_strategies
from competition import Competition
import pandas as pd

bp = Blueprint('routes', __name__)
competition = Competition()

@bp.route('/')
def index():
    strategies = import_strategies("strategies")
    return render_template('index.html', strategies=strategies)

@bp.route('/results', methods=['POST'])
def results():
    selected_strategies = request.form.getlist('strategies')
    result_df = competition.start_competition(selected_strategies)

    strategy_scores = pd.concat([
        result_df[['Strategy1', 'Author1', 'Startegy1_score']].rename(columns={'Strategy1': 'Strategy', 'Author1': 'Author', 'Startegy1_score': 'Score'}),
        result_df[['Strategy2', 'Author2', 'Strategy2_score']].rename(columns={'Strategy2': 'Strategy', 'Author2': 'Author', 'Strategy2_score': 'Score'})
    ])

    strategy_total_scores = strategy_scores.groupby(['Strategy', 'Author'])['Score'].sum().reset_index().sort_values('Score', ascending=False)

    return render_template('results.html', strategy_total_scores=strategy_total_scores.to_dict(orient='records'))

@bp.route('/strategy/<strategy_name>')
def strategy_details(strategy_name):
    matches = competition.get_strategy_matches(strategy_name)
    return render_template('strategy_details.html', strategy_name=strategy_name, matches=matches)

