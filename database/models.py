from database import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    login = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(162),
        nullable=False
    )

    # Связь с таблицей статей
    articles = db.relationship(
        'Articles',
        backref='author',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.id}: {self.login}>'


class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Автор статьи
    login_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Заголовок
    title = db.Column(
        db.String(100),
        nullable=False
    )

    # Текст статьи
    article_text = db.Column(
        db.Text,
        nullable=False
    )

    # Публичность
    # True  — видна всем
    # False — только автору
    is_public = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # Избранное (для расширений)
    is_favorite = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    # Лайки
    likes = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    def __repr__(self):
        return f'<Article {self.id}: {self.title}>'
