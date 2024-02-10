from flaskapp import app
from flask import render_template

@app.route('/hello')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/')
def leaderboard():
    return render_template('leaderboard.html')
