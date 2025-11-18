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
    return render_template('lab5/lab5.html', login=session.get('login'))

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
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    # Используем функции для работы с БД
    conn, cur = db_connect()

    # Проверка существования пользователя
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    # Добавление нового пользователя
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/list')
def articles_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]

    cur.execute("SELECT * FROM articles WHERE user_id=%s;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

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
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]  # Теперь user_id определен
    
    # Вставляем статью в базу
    cur.execute("INSERT INTO articles(user_id, title, article_text) VALUES (%s, %s, %s);", 
                (user_id, title, article_text))
    
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
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]
    
    # Проверяем, принадлежит ли статья пользователю
    cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
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
    cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s AND user_id=%s;",
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
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]
    
    # Получаем данные статьи для отображения названия
    cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
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
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return redirect('/lab5/login')
    
    user_id = user["id"]
    
    # Удаляем статью
    cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')