from flask import Blueprint, request, render_template, redirect, url_for
from database import db
from database.models import Users, Articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, func

lab8 = Blueprint('lab8', __name__)

# ---------------- ГЛАВНАЯ ----------------
@lab8.route('/lab8/')
def lab():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/lab8.html', username=username)


# ---------------- ЛОГИН ----------------
@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('lab8.article_list'))

    next_page = (
        request.args.get('next')
        or request.form.get('next')
        or url_for('lab8.article_list')
    )

    if request.method == 'POST':
        login_form = request.form.get('login', '').strip()
        password_form = request.form.get('password', '').strip()
        remember = request.form.get('remember') == 'on'

        if not login_form or not password_form:
            return render_template(
                'lab8/login.html',
                error='Логин и пароль не могут быть пустыми',
                next=next_page
            )

        user = Users.query.filter_by(login=login_form).first()

        if user and check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return redirect(next_page)

        return render_template(
            'lab8/login.html',
            error='Ошибка входа: логин и/или пароль неверны',
            next=next_page
        )

    return render_template('lab8/login.html', next=next_page)


# ---------------- РЕГИСТРАЦИЯ ----------------
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('lab8.article_list'))

    if request.method == 'POST':
        login_form = request.form.get('login', '').strip()
        password_form = request.form.get('password', '').strip()

        if not login_form:
            return render_template(
                'lab8/register.html',
                error='Имя пользователя не может быть пустым'
            )

        if not password_form:
            return render_template(
                'lab8/register.html',
                error='Пароль не может быть пустым'
            )

        if Users.query.filter_by(login=login_form).first():
            return render_template(
                'lab8/register.html',
                error='Такой пользователь уже существует'
            )

        new_user = Users(
            login=login_form,
            password=generate_password_hash(password_form)
        )
        db.session.add(new_user)
        db.session.commit()

        # автоматический логин
        login_user(new_user, remember=True)

        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/register.html')


# ---------------- ВЫХОД ----------------
@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('lab8.lab'))


# ---------------- СПИСОК СТАТЕЙ + ПОИСК ----------------
@lab8.route('/lab8/articles/')
def article_list():
    search = request.args.get('q', '').strip()

    # базовый фильтр
    if current_user.is_authenticated:
        base_filter = or_(
            Articles.login_id == current_user.id,   # свои
            Articles.is_public == True               # публичные
        )
    else:
        base_filter = Articles.is_public == True    # только публичные

    query = Articles.query.filter(base_filter)

    # поиск (регистронезависимый)
    articles = query.order_by(Articles.id.desc()).all()

    if search:
        search_lower = search.lower()

        articles = [
            article for article in articles
            if search_lower in article.title.lower()
            or search_lower in article.article_text.lower()
        ]

    return render_template(
        'lab8/articles.html',
        articles=articles,
        search=search,
        username=current_user.login if current_user.is_authenticated else 'anonymous'
    )


# ---------------- СОЗДАНИЕ ----------------
@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        text = request.form.get('article_text', '').strip()
        is_public = request.form.get('is_public') == 'on'

        if not title or not text:
            return render_template(
                'lab8/create.html',
                error='Заголовок и текст статьи не могут быть пустыми'
            )

        article = Articles(
            title=title,
            article_text=text,
            is_public=is_public,
            login_id=current_user.id
        )
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/create.html')


# ---------------- РЕДАКТИРОВАНИЕ ----------------
@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = Articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return 'Нет доступа', 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        text = request.form.get('article_text', '').strip()
        is_public = request.form.get('is_public') == 'on'

        if not title or not text:
            return render_template(
                'lab8/edit.html',
                article=article,
                error='Заголовок и текст статьи не могут быть пустыми'
            )

        article.title = title
        article.article_text = text
        article.is_public = is_public
        db.session.commit()

        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/edit.html', article=article)


# ---------------- УДАЛЕНИЕ ----------------
@lab8.route('/lab8/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete(article_id):
    article = Articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return 'Нет доступа', 403

    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('lab8.article_list'))
