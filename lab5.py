from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session, current_app
from functools import wraps
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route("/lab5/")
def lab():
    login = session.get('login')
    real_name = None
    
    if login:
        conn, cur = db_connect()
        cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        if user:
            real_name = user['real_name']
        db_close(conn, cur)
    
    return render_template('lab5/lab5.html', login=login, real_name=real_name)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='saymon_bogdanov_knowledge_base',
            user='saymon_bogdanov_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните все поля")

    # Используем функции для работы с БД
    conn, cur = db_connect()

    # Проверка существования пользователя
    cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    
    # Получаем реальное имя для отображения
    real_name = user.get('real_name')
    
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login, real_name=real_name)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name')  # Новое поле

    if not login or not password or not real_name:
        return render_template('lab5/register.html', error='Заполните все поля')

    # Используем функции для работы с БД
    conn, cur = db_connect()

    # Проверка существования пользователя
    cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    # Хешируем пароль
    password_hash = generate_password_hash(password)
    
    # Добавление нового пользователя с реальным именем
    cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", 
                (login, password_hash, real_name))
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/list')
def articles_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]

    # Получаем статьи пользователя, любимые статьи выводятся первыми
    cur.execute("""
        SELECT * FROM articles 
        WHERE user_id=? 
        ORDER BY is_favorite DESC, id DESC;
    """, (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    # Обработка POST-запроса
    title = request.form.get('title')
    article_text = request.form.get('article_text')

     # ВАЛИДАЦИЯ: проверка на пустые поля
    if not title or not article_text:
        error_message = "Заполните все поля: название и текст статьи"
        return render_template('lab5/create_article.html', error=error_message)
    
    # ВАЛИДАЦИЯ: проверка на пробельные символы
    if title.strip() == "" or article_text.strip() == "":
        error_message = "Поля не могут содержать только пробелы"
        return render_template('lab5/create_article.html', error=error_message)
    
    conn, cur = db_connect()
    
    # Получаем ID пользователя по логину
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]  # Теперь user_id определен
    
    # Вставляем статью в базу
    cur.execute("INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);", 
            (user_id, title, article_text, False, False))
    
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/logout')
def logout():
    # Удаляем логин из сессии
    session.pop('login', None)
    # Перенаправляем на главную страницу
    return redirect('/lab5')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Получаем ID пользователя
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]
    
    # Проверяем, принадлежит ли статья пользователю
    cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для её редактирования", 403
    
    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                             article=article, 
                             article_id=article_id)
    
    # Обработка POST-запроса (обновление статьи)
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    # Валидация
    if not title or not article_text:
        db_close(conn, cur)
        error_message = "Заполните все поля: название и текст статьи"
        return render_template('lab5/edit_article.html', 
                             article=article, 
                             article_id=article_id,
                             error=error_message)
    
    if title.strip() == "" or article_text.strip() == "":
        db_close(conn, cur)
        error_message = "Поля не могут содержать только пробелы"
        return render_template('lab5/edit_article.html', 
                             article=article, 
                             article_id=article_id,
                             error=error_message)
    
    # Обновляем статью в базе данных
    cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=? AND user_id=?;",
                (title, article_text, article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>')
def confirm_delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Получаем ID пользователя и данные статьи
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]
    
    # Получаем данные статьи для отображения названия
    cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для её удаления", 403
    
    db_close(conn, cur)
    return render_template('lab5/confirm_delete.html', 
                         article_title=article['title'], 
                         article_id=article_id)

@lab5.route('/lab5/delete/<int:article_id>/confirm')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Получаем ID пользователя
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]
    
    # Удаляем статью
    cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def users_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Получаем всех пользователей (только логины и имена)
    cur.execute("SELECT login, real_name FROM users ORDER BY id;")
    users = cur.fetchall()
    
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users, login=login)


@lab5.route('/lab5/change-profile', methods=['GET', 'POST'])
def change_profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        conn, cur = db_connect()
        cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        real_name = user['real_name'] if user else ''
        db_close(conn, cur)
        
        return render_template('lab5/change_profile.html', 
                             login=login, 
                             real_name=real_name,
                             error=None)
    
    # Обработка POST-запроса
    new_real_name = request.form.get('real_name')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    conn, cur = db_connect()
    
    # Получаем текущие данные пользователя
    cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    error = None
    
    # Проверка текущего пароля
    if current_password and not check_password_hash(user['password'], current_password):
        error = "Неверный текущий пароль"
    
    # Проверка подтверждения нового пароля
    elif new_password and new_password != confirm_password:
        error = "Новый пароль и подтверждение не совпадают"
    
    # Проверка минимальной длины пароля
    elif new_password and len(new_password) < 6:
        error = "Пароль должен содержать минимум 6 символов"
    
    # Проверка имени
    elif not new_real_name or new_real_name.strip() == "":
        error = "Имя не может быть пустым"
    
    if error:
        db_close(conn, cur)
        return render_template('lab5/change_profile.html', 
                             login=login, 
                             real_name=new_real_name,
                             error=error)
    
    # Обновление данных
    if new_password:
        # Обновляем имя и пароль
        password_hash = generate_password_hash(new_password)
        cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;",
                    (new_real_name, password_hash, login))
    else:
        # Обновляем только имя
        cur.execute("UPDATE users SET real_name=? WHERE login=?;",
                    (new_real_name, login))
    
    db_close(conn, cur)
    
    # Обновляем сессию если нужно
    session['login'] = login
    
    return render_template('lab5/profile_updated.html', 
                         login=login, 
                         real_name=new_real_name)
                

@lab5.route('/lab5/public-articles')
def public_articles():
    login = session.get('login')
    
    conn, cur = db_connect()

    # Получаем все публичные статьи, отсортированные по дате
    cur.execute("""
        SELECT a.*, u.real_name as author_name 
        FROM articles a 
        JOIN users u ON a.user_id = u.id 
        WHERE a.is_public = TRUE 
        ORDER BY a.id DESC;
    """)
    public_articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/public_articles.html', 
                         articles=public_articles, 
                         login=login)        


# Маршруты для управления избранным
@lab5.route('/lab5/favorite/<int:article_id>')
def favorite_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Проверяем принадлежность статьи
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if user:
        user_id = user["id"]
        cur.execute("UPDATE articles SET is_favorite=TRUE WHERE id=? AND user_id=?;", 
                    (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/unfavorite/<int:article_id>')
def unfavorite_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Проверяем принадлежность статьи
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if user:
        user_id = user["id"]
        cur.execute("UPDATE articles SET is_favorite=FALSE WHERE id=? AND user_id=?;", 
                    (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

# Маршруты для управления публичностью
@lab5.route('/lab5/make-public/<int:article_id>')
def make_article_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Проверяем принадлежность статьи
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if user:
        user_id = user["id"]
        cur.execute("UPDATE articles SET is_public=TRUE WHERE id=? AND user_id=?;", 
                    (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/make-private/<int:article_id>')
def make_article_private(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    # Проверяем принадлежность статьи
    cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    
    if user:
        user_id = user["id"]
        cur.execute("UPDATE articles SET is_public=FALSE WHERE id=? AND user_id=?;", 
                    (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')