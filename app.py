from flask import Flask,  render_template,  url_for,  request
import pickle
import numpy as np
from csv import writer
import pandas as pd


India_T20=pd.read_csv(r".\data\India T20I.csv",delimiter=",")
India_T20=India_T20.drop(['ball'], axis = 1)
India_T20=India_T20.set_index(["Match ID","Playing Against"])

match_details=pd.read_csv(r".\data\Match details.csv",delimiter=",")
match_details=match_details.drop(['date','Umpire1','Umpire2'],axis=1)

venue_names=[]
team2_names=[]
innings_played=[1,2]
batsman_names=[]
over=[]
bowler_names=[]

for g,f in match_details.groupby("Venue"):
    venue_names.append(g.lower())
for g,f in India_T20.groupby("Playing Against"):
    team2_names.append(g.lower())

India_Batting=India_T20[India_T20["Batting"]=="India"]
for group,frame in India_Batting.groupby("Striker"):
    batsman_names.append(group.lower())
for g,f in India_T20.groupby("Over type"):
    over.append(g.lower())

for g,f in India_T20.groupby("Bowler"):
    bowler_names.append(g.lower())


app = Flask(__name__)

runrate_model = pickle.load(open('runrate.pkl',  'rb'))
economy_model = pickle.load(open('economy.pkl',  'rb'))
strikerate_model = pickle.load(open('strikerate.pkl',  'rb'))
wickets_model = pickle.load(open('wickets.pkl',  'rb'))

@app.route('/')
def main():
    return render_template('Main/index.html')

@app.route('/home')
def home():
    return render_template('Main/index.html')

@app.route('/aboutproject')
def aboutproject():
    return render_template('Main/AboutProject.html')

@app.route('/cricket_predictions')
def parameters_prediction():
    return render_template('Main/Cricket Predictions.html')

@app.route('/runrate')
def runrate():
    return render_template('Runrate/Input/Runrate Input.html')

@app.route('/runrate_predict', methods=['GET', 'POST'])
def runrate_predict():
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        print("Hello")
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names)):
        return render_template('Runrate/Input/Runrate Input.html', message="Please give the correct information")
    else:
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[v,innings,o]]
        prediction=round(runrate_model.predict(data)[0],2)
        return render_template('Runrate/Output/Runrate Output.html', result=prediction)
        
@app.route('/player_stats')
def player_stats():
    return render_template('Player stats/Player stats.html')

@app.route('/strikerate')
def strikerate():
    return render_template('Player stats/Strikerate/Input/Strikerate Input.html')


@app.route('/strikerate_predict', methods=['GET', 'POST'])
def strikerate_predict():
    player=request.form['player'].lower()
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        print("Hello")
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    overtype=request.form['overtype'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names) or (player not in batsman_names) or (overtype not in over)):
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    else:
        p=batsman_names.index(player)
        ov=over.index(overtype)
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[p,o,innings,v,ov]]
        prediction=round(strikerate_model.predict(data)[0],2)
        return render_template('Player stats/Strikerate/Output/Strikerate Output.html', result=prediction)

@app.route('/economy')
def economy():
    return render_template('Player stats/Economy/Input/Economy Input.html')

@app.route('/economy_predict', methods=['GET', 'POST'])
def economy_predict():
    player=request.form['player'].lower()
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        print("Hello")
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    overtype=request.form['overtype'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names) or (player not in bowler_names) or (overtype not in over)):
        return render_template('Player stats/Economy/Input/Economy Input.html', message="Please give the correct information")
    else:
        p=bowler_names.index(player)
        ov=over.index(overtype)
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[p,o,innings,v,ov]]
        prediction=round(economy_model.predict(data)[0],2)
        return render_template('Player stats/Economy/Output/Economy Output.html', result=prediction)

@app.route('/wickets')
def wickets():
    return render_template('Player stats/Wickets/Input/Wickets Input.html')

@app.route('/wickets_predict', methods=['GET', 'POST'])
def wickets_predict():
    player=request.form['player'].lower()
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        print("Hello")
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    overtype=request.form['overtype'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names) or (player not in bowler_names) or (overtype not in over)):
        return render_template('Player stats/Wickets/Input/Wickets Input.html', message="Please give the correct information")
    else:
        p=bowler_names.index(player)
        ov=over.index(overtype)
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[p,o,innings,v,ov]]
        prediction=round(wickets_model.predict(data)[0],2)
        return render_template('Player stats/Wickets/Output/Wickets Output.html', result=prediction)
        
if __name__ == '__main__':
    app.run(debug=True)
