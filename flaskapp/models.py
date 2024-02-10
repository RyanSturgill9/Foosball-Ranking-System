from datetime import datetime, timezone
from flaskapp import db, bcrypt
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    _password = db.Column(db.String, nullable=False, default='Something has gone terribly wrong') # Do not directly change the _password property. Use set_password() and check_password()
    email = db.Column(db.String, unique=True, nullable=False)
    email_is_verified = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_timestamp = db.Column(db.DateTime)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    elo = db.Column(db.Integer, nullable=False, default=1000)
    games_played = db.Column(db.Integer, nullable=False, default=0)
    account_created_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    last_login_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    profile_picture = db.Column(db.String)
    description = db.Column(db.Text)

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
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entered_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    player1_score = db.Column(db.Integer, nullable=False, default=0)
    player2_score = db.Column(db.Integer, nullable=False, default=0)
    game_completed = db.Column(db.Boolean, default=False, nullable=False)
    score_pad = db.Column(db.String)
    data_entered_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    game_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
