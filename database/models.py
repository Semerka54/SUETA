from . import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'user'  # Явное имя таблицы, чтобы совпадало с FK
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)

    # Связь с таблицей Articles (опционально, удобно для ORM)
    articles = db.relationship('Articles', backref='user', lazy=True)


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)
    likes = db.Column(db.Integer, default=0)
