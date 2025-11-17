from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session
from functools import wraps
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

@lab5.route("/lab5/")
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните все поля")

# Подключение к базе данных
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='saymon_bogdanov_knowledge_base',
        user='saymon_bogdanov_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory = RealDictCursor)

    # Проверка существования пользователя (исправлен SQL-запрос)
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    if user['password'] != password:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    session['login'] = login
    cur.close()
    conn.close()
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    # Получение данных из формы должно быть внутри функции
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    # Подключение к базе данных
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='saymon_bogdanov_knowledge_base',
        user='saymon_bogdanov_knowledge_base',
        password='123'
    )
    cur = conn.cursor()

    # Проверка существования пользователя (исправлен SQL-запрос)
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))

    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    # Добавление нового пользователя (исправлен SQL-запрос)
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/list')
def articles_list():
    return "Список статей"

@lab5.route('/lab5/create')
def create_article():
    return "Создать статью"