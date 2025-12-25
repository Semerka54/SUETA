import os
from os import path
from flask import Flask, render_template
from flask_login import LoginManager
from rgz import rgz
from rgz.db_rgz import db_rgz
from rgz.models import Admin

# =====================================================
# Flask app
# =====================================================
app = Flask(__name__, template_folder='templates')

# =====================================================
# CONFIG
# =====================================================
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '777')
base_dir = path.dirname(path.realpath(__file__))
rgz_db_path = path.join(base_dir, "rgz.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{rgz_db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =====================================================
# INIT DATABASE
# =====================================================
db_rgz.init_app(app)

# =====================================================
# Login manager
# =====================================================
login_manager = LoginManager()
login_manager.login_view = 'rgz.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Загружаем администратора по id
    return Admin.query.get(int(user_id))

# =====================================================
# REGISTER BLUEPRINTS
# =====================================================
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
    from flask import request, url_for
    import datetime

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
        <head><meta charset="utf-8"><title>404 Страница не найдена</title></head>
        <body style="font-family: Arial; text-align: center;">
            <h1>404 Страница не найдена</h1>
            <p>Запрошенная страница не существует</p>
            <img src="{img_path}" width="300"><br><br>
            <b>IP:</b> {ip}<br>
            <b>Время:</b> {time}<br><br>
            <a href="/">На главную</a>
            <h3>Журнал</h3>{log_html}
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