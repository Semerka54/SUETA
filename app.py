import datetime
import os
from os import path

from flask import Flask, render_template, request, url_for
from flask_login import LoginManager

# ===== RGZ =====
from rgz import rgz
from rgz.db_rgz import db_rgz

# ===== LABS =====
from database import db
from database.models import Users

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9

# =====================================================
# Flask app
# =====================================================

app = Flask(__name__)

# =====================================================
# Login manager
# =====================================================

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return Users.query.get(int(login_id))

# =====================================================
# CONFIG
# =====================================================

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '777')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

# -------- Основная БД (лабы) --------
if app.config['DB_TYPE'] == 'postgres':
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql://saymon_bogdanov_orm:123@127.0.0.1:5432/saymon_bogdanov_orm'
    )
else:
    base_dir = path.dirname(path.realpath(__file__))
    main_db_path = path.join(base_dir, "saymon_bogdanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{main_db_path}'

# -------- БД РГЗ (ОТДЕЛЬНАЯ SQLite) --------
rgz_db_path = path.join(base_dir, "rgz.db")
app.config['SQLALCHEMY_BINDS'] = {
    'rgz': f'sqlite:///{rgz_db_path}'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =====================================================
# INIT DATABASES
# =====================================================

db.init_app(app)        # БД лабораторных
db_rgz.init_app(app)    # БД РГЗ

# =====================================================
# REGISTER BLUEPRINTS
# =====================================================

# лабораторные
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)

# РГЗ
app.register_blueprint(rgz)

# =====================================================
# ROUTES
# =====================================================

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# =====================================================
# ERROR HANDLERS
# =====================================================

log_data = []

@app.errorhandler(404)
def not_found(error):
    img_path = url_for("static", filename="404.jpg")

    ip = request.remote_addr
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url

    log_entry = f"[{time}], пользователь {ip} зашёл на адрес: {url}"
    log_data.append(log_entry)

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
        </head>
        <body style="font-family: Arial; text-align: center;">
            <h1>404 Страница не найдена</h1>
            <p>Запрошенная страница не существует</p>
            <img src="{img_path}" width="300"><br><br>
            <b>IP:</b> {ip}<br>
            <b>Время:</b> {time}<br><br>
            <a href="/">На главную</a>
            <h3>Журнал</h3>
            {log_html}
        </body>
    </html>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    return """
    <html>
        <head><title>Ошибка 500</title></head>
        <body style="font-family: Arial; text-align: center;">
            <h1>500 Внутренняя ошибка сервера</h1>
            <p>Попробуйте позже</p>
        </body>
    </html>
    """, 500
