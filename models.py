from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    '''connects to database'''
    db.app=app
    db.init_app(app)
    #db.drop_all()
    db.create_all()

class User(db.Model):
    '''creates a user and hosts methods for registering and authenticating'''

    __tablename__='users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    feedback = db.relationship('Feedback', backref='user', cascade='all, delete-orphan', passive_deletes=True)


    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """register user with hashed password and returns user instance"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """validates user information and returns instance of user or false"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    '''creates a feedback record'''

    __tablename__='feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, db.ForeignKey('users.username', ondelete='CASCADE'))