from datetime import datetime, timezone
from flaskapp import db, bcrypt
from flask_login import UserMixin
import secrets

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    _password = db.Column(db.String, nullable=False, default=secrets.token_urlsafe(32)) # Do not directly change the _password property. Use set_password() and check_password()
    email = db.Column(db.String, unique=True, nullable=False)
    email_is_verified = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_timestamp = db.Column(db.DateTime)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    elo = db.Column(db.Integer, nullable=False, default=1000)
    account_created_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_login_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    profile_picture = db.Column(db.String)
    description = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False, nullable=False) # Can remove people
    is_verified = db.Column(db.Boolean, default=False, nullable=False) # Can add games
    is_referee = db.Column(db.Boolean, default=False, nullable=False) # Can verify games
    play_count = db.Column(db.Integer, nullable=False, default=0)
    officiate_count = db.Column(db.Integer, nullable=False, default=0)

    '''
    Added by Tournament backref:
    - tournaments_played
    - tournaments_officiated
    '''

    # Relationships
    awards = db.relationship('Award', secondary='awardee_award', backref='awardees')
    games_played1 = db.relationship('Game', backref='player1', foreign_keys='Game.player1_id')
    games_played2 = db.relationship('Game', backref='player2', foreign_keys='Game.player2_id')
    games_officiated = db.relationship('Game', backref='referee', foreign_keys='Game.referee_id')

    def set_password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')
        return True
 
    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    def __repr__(self):
        return f'<User id={self.id}, username={self.username}, email={self.email}>'

# Model created with idea that some games may have info entered incompletely or be modified
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    player1_score = db.Column(db.Integer, nullable=False, default=0)
    player2_score = db.Column(db.Integer, nullable=False, default=0)
    game_completed = db.Column(db.Boolean, default=False, nullable=False)
    score_pad = db.Column(db.String)
    data_entered_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    game_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Foreign keys
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entered_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))

    '''
    Added by Tournament backref:
    - tournament

    Added by User backref:
    - player1
    - player2
    - referee
    '''

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    difficulty_level = db.Column(db.String)
    elimination_type = db.Column(db.String) # single-elim, double-elim, round-robin

    # Relationships
    games = db.relationship('Game', backref='tournament')
    players = db.relationship('User', secondary='tournament_player', backref='tournaments_played')
    referees = db.relationship('User', secondary='tournament_referee', backref='tournaments_officiated')

tournament_player = db.Table('tournament_player',
                             db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id')),
                             db.Column('player_id', db.Integer, db.ForeignKey('user.id')),
                             )
tournament_referee = db.Table('tournament_referee',
                              db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id')),
                              db.Column('referee_id', db.Integer, db.ForeignKey('user.id')),
                              )
awardee_award = db.Table('awardee_award',
                         db.Column('awardee_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('award_id', db.Integer, db.ForeignKey('award.id')),
                         )

class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    # Foreign keys
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))

    '''
    Added by User backref:
    - awardees
    '''