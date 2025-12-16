from flask import Blueprint, request, render_template
from database import db
from database.models import Users, Articles
from werkzeug.security import generate_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', username='anonymous')

@lab8.route('/lab8/login')
def login():
    return render_template('lab8/login.html')

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

@lab8.route('/lab8/articles')
def articles():
    return render_template('lab8/articles.html')

@lab8.route('/lab8/create')
def create():
    return render_template('lab8/create.html')
