import datetime
import os
from os import path

from flask import Flask, render_template, request, url_for
from rgz import rgz
from rgz.db_rgz import db_rgz
from database import db
from database.models import Users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return Users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '777')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql://saymon_bogdanov_orm:123@127.0.0.1:5432/saymon_bogdanov_orm'
    )
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "saymon_bogdanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# список для хранения лога
log_data = []

@app.errorhandler(404)
def not_found(error):
    img_path = url_for("static", filename="404.jpg")  
    
    # данные о пользователе
    ip = request.remote_addr
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url

    # добавляем запись в лог
    log_entry = f"[{time}], пользователь {ip} зашёл на адрес: {url}"
    log_data.append(log_entry)

    # формируем HTML список журнала
    log_html = "<ul>"
    for entry in log_data:
        log_html += f"<li>{entry}</li>"
    log_html += "</ul>"

    return f"""
    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>404 Страница не найдена</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    text-align: center;
                    padding: 50px;
                    margin: 0;
                }}
                h1 {{
                    font-size: 3em;
                    color: #e74c3c;
                }}
                p {{
                    font-size: 1.2em;
                    color: #555;
                }}
                img {{
                    width: 300px;
                    margin-top: 20px;
                }}
                footer {{
                    margin-top: 40px;
                    font-size: 0.9em;
                    color: gray;
                    text-align: center;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                    font-weight: bold;
                }}
                .journal {{
                    margin-top: 40px;
                    text-align: left;
                    max-width: 800px;
                    margin-left: auto;
                    margin-right: auto;
                }}
            </style>
        </head>
        <body>

            <h1>404 Страница не найдена</h1>
            <p>Ой, мы не можем найти эту страницу. Возможно, она была удалена или никогда не существовала.</p>
            <img src="{img_path}" alt="Не найдено">

            <p><b>Ваш IP:</b> {ip}</p>
            <p><b>Дата и время:</b> {time}</p>

            <footer>
                <p>Возвращайтесь на <a href="/">главную страницу</a>.</p>
            </footer>

            <div class="journal">
                <h2>Журнал:</h2>
                {log_html}
            </div>

        </body>
    </html>
    """, 404


@app.errorhandler(500)
def internal_error(error):
    return """
    <!doctype html>
    <html>
        <head><title>Ошибка 500</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>500 Внутренняя ошибка сервера</h1>
            <p>Произошла ошибка на сервере. Пожалуйста, попробуйте позже.</p>
        </body>
    </html>
    """, 500