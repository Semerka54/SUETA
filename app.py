from flask import Flask, url_for, request, redirect, render_template, Response, abort
import datetime
from lab1 import lab1
from lab2 import lab2

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)


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