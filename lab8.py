from flask import Blueprint, request, render_template, session, redirect, url_for
from database import db
from database.models import Users, Articles
from flask_login import login_user, login_required, current_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    # Если пользователь авторизован, берем его логин, иначе "anonymous"
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/lab8.html', username=username)


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    # Берём next из query string (GET) или формы (POST)
    next_page = request.args.get('next') if request.method == 'GET' else request.form.get('next')

    if request.method == 'POST':
        login_form = request.form.get('login', '').strip()
        password_form = request.form.get('password', '').strip()

        # Проверка на пустые поля
        if not login_form or not password_form:
            return render_template('lab8/login.html',
                                   error='Логин и пароль не могут быть пустыми',
                                   next=next_page)

        user = Users.query.filter_by(login=login_form).first()

        if user and check_password_hash(user.password, password_form):
            login_user(user, remember=False)
            return redirect(next_page or url_for('lab8.lab'))

        # Неверный логин или пароль
        return render_template('lab8/login.html',
                               error='Ошибка входа: логин и/или пароль неверны',
                               next=next_page)

    # GET-запрос
    return render_template('lab8/login.html', next=next_page)


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()

    # Проверка на пустые поля
    if not login_form:
        return render_template('lab8/register.html', 
                               error='Имя пользователя не может быть пустым',
                               username='anonymous')
    if not password_form:
        return render_template('lab8/register.html', 
                               error='Пароль не может быть пустым',
                               username='anonymous')

    # Проверка существующего пользователя
    login_exists = Users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                               error='Такой пользователь уже существует',
                               username='anonymous')
    
    # Создание нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = Users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return render_template('lab8/register.html', 
                           success='Пользователь успешно зарегистрирован',
                           username=login_form)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    articles = Articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=articles, username=current_user.login)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        text = request.form.get('article_text', '').strip()

        if not title or not text:
            return render_template('lab8/create.html', 
                                   error='Заголовок и текст статьи не могут быть пустыми',
                                   username=current_user.login)

        new_article = Articles(title=title, article_text=text, login_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/create.html', username=current_user.login)


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = Articles.query.get_or_404(article_id)
    if article.login_id != current_user.id:
        return "Нет доступа", 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        text = request.form.get('article_text', '').strip()

        if not title or not text:
            return render_template('lab8/edit.html', article=article, 
                                   error='Заголовок и текст статьи не могут быть пустыми',
                                   username=current_user.login)

        article.title = title
        article.article_text = text
        db.session.commit()
        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/edit.html', article=article, username=current_user.login)


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete(article_id):
    article = Articles.query.get_or_404(article_id)
    if article.login_id != current_user.id:
        return "Нет доступа", 403

    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('lab8.article_list'))
