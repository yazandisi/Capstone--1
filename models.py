import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Category_Game(db.Model):
    """Model for catagory games"""
    __tablename__ = 'category_games'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    category_id = db.Column(
        db.Integer, 
        db.ForeignKey('categories.id'))
        
    game_id = db.Column(
        db.Integer,
        db.ForeignKey('games.id'))

class Game(db.Model):
    """Model for songs"""
    __tablename__ = 'games'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    title = db.Column(db.Text, nullable=False)
    genre = db.Column(db.Text, nullable=False)
    company = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    favorite = db.Column(db.Boolean)
    api_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="games")

class Category(db.Model):
    """Model for playlists"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True)
    
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)


    @classmethod
    def register(cls, username, pwd):
        """Return user with hashed password"""
        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct
        Return user if valid; Return False if not
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False