from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class."""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

    def __repr__(self):
        u = self

        return f"<User {u.username} {u.password} {u.email} {u.first_name} {u.last_name}>"

    @classmethod
    def register(cls, username, pwd, email, first, last):
        """Register user with hashed password and return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username,
                   password=hashed_utf8,
                   email=email,
                   first_name=first,
                   last_name=last)

    @classmethod
    def authenticate(cls, username, password):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback class"""

    __tablename__ = "feedback_all"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String,
                         db.ForeignKey("users.username"))

    user = db.relationship("User",
                           backref="feedback")

    def __repr__(self):
        f = self

        return f"<Feedback {f.id} {f.title} {f.content} {f.username}>"