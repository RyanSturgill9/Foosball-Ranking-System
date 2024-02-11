from flaskapp import app, db
from flaskapp.models import User, Game

user1_data = {
    'username': 'testuser1',
    'display_name': 'Test User 1',
    'email': 'user1@test.com',
    'firstname': 'Userone',
    'lastname': 'Test',
    'description': 'I\'m addicted to foosball...',
}
user1 = User(**user1_data)
user1.set_password('helloworldhelloworld')

user2_data = {
    'username': 'testuser2',
    'display_name': 'Test User 2',
    'email': 'user2@test.com',
    'firstname': 'Usertwo',
    'lastname': 'Test',
    'description': 'I\'m addicted to foosball...',
}
user2 = User(**user2_data)
user2.set_password('helloworldhelloworld')

user3_data = {
    'username': 'testuser3',
    'display_name': 'Test User 3',
    'email': 'user3@test.com',
    'firstname': 'Userthree',
    'lastname': 'Test',
    'description': 'I\'m addicted to foosball...',
}
user3 = User(**user3_data)
user3.set_password('helloworldhelloworld')

referee_data = {
    'username': 'testreferee',
    'display_name': 'Test Referee',
    'email': 'referee@test.com',
    'firstname': 'Referee',
    'lastname': 'Test',
    'description': 'You\'re addicted to foosball...',
}
referee = User(**referee_data)
referee.set_password('helloworldhelloworld')

# Doesn't simulate game

game1_data = {
    'player1_id': 1,
    'player2_id': 2,
    'referee_id': 4,
    'entered_by_id': 3,
    'player1_score': 10,
    'player2_score': 5,
    'game_completed': True,
}
game1 = Game(**game1_data)

user1.games_played.append(game1)

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(game1)

    db.session.commit()