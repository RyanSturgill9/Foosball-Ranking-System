from flaskapp import app
from flask import render_template, jsonify

@app.route('/hello')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/add-game', methods=['POST'])
def add_game():
    return jsonify({'response': 'Game added successfully'})