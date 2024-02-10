from datetime import datetime
from flaskapp import db, bcrypt

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password = db.Column(db.String, nullable=False, default='Something has gone terribly wrong') # Do not directly change the _password property. Use set_password() and check_password()
    email = db.Column(db.String, unique=True, nullable=False)
    email_is_verified = db.Column(db.Boolean, nullable=False, default=False)
    account_created_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    email_confirmed_timestamp = db.Column(db.DateTime)
    last_login_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    profile_picture = db.Column(db.String)
    description = db.Column(db.Text)
    role = db.Column(db.String, default='user')

    def set_password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')
        return True
 
    def check_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    def __repr__(self):
        return f'<User id={self.id}, username={self.username}, email={self.email}>'
    
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String, nullable=False)
    last = db.Column(db.String, nullable=False)
    elo = db.Column(db.Integer, nullable=False, default=1000)