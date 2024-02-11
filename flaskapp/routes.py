from flaskapp import app, db, login_manager
from flask import render_template, jsonify, redirect, url_for, flash
from flaskapp.forms import LoginForm, RegisterForm, GameForm
from flaskapp.models import User, Game
from flask_login import login_required, current_user, login_user, logout_user
from datetime import datetime, timezone
from flaskapp.elo import calculate_elo

@app.route('/hello')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/')
def leaderboard():
    query = db.select(User).order_by(User.elo.desc())
    users = db.session.execute(query).scalars()
    return render_template('leaderboard.html', current_user=current_user, users=users,)

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
        profile_picture=user.profile_picture,
        games_played=user.games_played)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
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
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one()
        if user and user.check_password(form.password.data):
            login_user(user)
            user.last_login_timestamp = datetime.now(timezone.utc)
            db.session.commit()
            return redirect(url_for('profile', id=user.id))
        flash('Login failed')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('leaderboard'))


@app.route('/submit-game', methods=['GET', 'POST'])
@login_required
def submit_game():
    form = GameForm()
    if form.validate_on_submit():
        game = Game(
            player1_id=form.player1_id.data,
            player1_score=form.player1_score.data,
            player2_id=form.player2_id.data,
            player2_score=form.player2_score.data,
            referee_id=form.referee_id.data,
            entered_by_id=current_user.id,
            game_completed=True,)
        db.session.add(game)

        player1 = User.query.get(form.player1_id.data)
        player2 = User.query.get(form.player2_id.data)
        if form.player1_score.data > form.player2_score.data:
            player1.elo, player2.elo = calculate_elo(player1.elo, player2.elo)
        elif form.player2_score.data > form.player1_score.data:
            player2.elo, player1.elo = calculate_elo(player2.elo, player1.elo)
        player1.play_count += 1
        player2.play_count += 1

        db.session.commit()
        
        flash('Success')
    return render_template('submit-game.html', form=form)