from flask import Blueprint, render_template, request, session, jsonify
from arena import Arena
from util import import_strategies
from competition import Competition
import pandas as pd
import json

bp = Blueprint('routes', __name__)
competition = Competition()

@bp.route('/')
def index():
    strategies = import_strategies("strategies")
    return render_template('index.html', strategies=strategies)


@bp.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        selected_strategies = request.form.getlist('strategies')
        rounds = int(request.form.get('runs'))
        games = int(request.form.get('games'))
        points_per_game = int(request.form.get('points_per_game'))

        result_df = competition.start_competition(selected_strategies, 
                                                  rounds = rounds, 
                                                  games = games, 
                                                  points_per_game = points_per_game)
        
        #print(result_df)
        

        strategy_scores = pd.concat([
            result_df[['Strategy1', 'Author1', 'Startegy1_score']].rename(columns={'Strategy1': 'Strategy', 'Author1': 'Author', 'Startegy1_score': 'Score'}),
            result_df[['Strategy2', 'Author2', 'Strategy2_score']].rename(columns={'Strategy2': 'Strategy', 'Author2': 'Author', 'Strategy2_score': 'Score'})
        ])

        strategy_total_scores = strategy_scores.groupby(['Strategy', 'Author'])['Score'].sum().reset_index().sort_values('Score', ascending=False).round(3)
        
        #print(strategy_total_scores)
        
        top_scorers = strategy_total_scores.to_dict(orient = 'records')

        # Store the results in the session
        session['result_df'] = result_df.to_dict(orient='records')
        session['results'] = top_scorers

    else:
        # Retrieve results from the session if available
        top_scorers = session.get('results', None)

    if len(top_scorers)>0:
        return render_template('results.html', strategy_total_scores=top_scorers)
    else:
        return render_template('index.html', error="No results available. Please run a new competition.")
        


@bp.route('/strategy/<strategy_name>')
def strategy_details(strategy_name):
    matches = competition.get_strategy_matches(strategy_name)
    #print(matches)
    return render_template('strategy_details.html', strategy_name=strategy_name, matches=matches)

@bp.route('/visualization')
def visualization():
    strategies = competition.get_unique_strategies()
    return render_template('visualization.html', strategies=json.dumps(strategies))

@bp.route('/get_data', methods=['GET'])
def get_data():
    result_df = session.get('result_df', [])
    #print(result_df)
    return jsonify(result_df)

