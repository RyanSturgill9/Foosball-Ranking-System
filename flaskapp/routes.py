from flaskapp import app, db, login_manager
from flask import render_template, jsonify, redirect, url_for, flash
from flaskapp import forms
from flaskapp.models import User, Game
from flask_login import login_required, current_user, login_user, logout_user

@app.route('/hello')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/')
def leaderboard():
    return render_template('leaderboard.html', current_user=current_user)

@app.route('/profile/<int:id>')
def profile(id):
    user = db.get_or_404(User, id)
    return render_template(
        'profile.html',
        username=user.username,
        display_name=user.display_name,
        firstname=user.firstname,
        lastname=user.lastname,
        elo=user.elo,
        description=user.description,
        profile_picture=user.profile_picture) # User information entered manually to prevent leaking data

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.Register()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            display_name=form.display_name.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile', id=user.id))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('profile', id=user.id))
        flash('Login failed')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('leaderboard'))


@app.route('/add-game', methods=['POST'])
def add_game():
    form = forms.Game()
    if form.validate_on_submit():
        return redirect('/')
    return jsonify({'response': 'Game added successfully'})