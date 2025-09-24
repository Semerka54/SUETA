from flask import Flask, url_for, request, redirect, render_template, Response
import datetime
app = Flask(__name__)

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Богданов Семён Андреевич"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
        img_path = url_for("static", filename="dub.jpg")
        css_path = url_for("static", filename="lab1.css")
        html_content = f'''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="{css_path}">
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="{img_path}" alt="Дуб">
            </body>
        </html>
        '''

        response = Response(html_content, content_type='text/html; charset=utf-8')
        response.headers['Content-Language'] = 'ru'
        response.headers['X-Custom-Header'] = 'This is a custom header'
        response.headers['X-Frame-Options'] = 'DENY'

        return response

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return f'''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: {count}
        <hr>
        Дата и время: {time}<br>
        Запрошенный адрес: {url}<br>
        Ваш IP адрес: {client_ip}<br>
        <br>
        <a href="/lab1/counter/reset">Сбросить счётчик</a>
    </body>
</html>
'''

@app.route('/lab1/counter/reset')
def counter_reset():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        Счётчик обнулён.<br>
        <a href="/lab1/counter">Назад к счётчику</a>
    </body>
</html>
'''

@app.route('/lab1/info')
def info():
    return redirect("author")

@app.route("/lab1/created")
def created():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>web-сервер на flask</h1>
            <a href="/lab1/author">author</a>
        </body>
    </html>
    """, 201

@app.route('/')
@app.route('/index')
def index():
    lab1_url = url_for('lab1')
    return f'''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f9;
                margin: 0; 
                padding-bottom: 60px; 
            }}
            footer {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 60px;
                background-color: #f4f4f9;
                color: gray;
                font-size: 0.9em;
                display: flex;
                align-items: center;
                justify-content: center;
                border-top: 1px solid #ccc;
            }}
        </style>
    </head>
    <body>

        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>

        <nav style="margin: 20px 0;">
            <a href="{lab1_url}">Первая лабораторная</a>
        </nav>

        <footer>
            Богданов Семён Андреевич, группа: ФБИ - 32, 3 курс, 2025
        </footer>

    </body>
</html>
'''

@app.route('/lab1')
def lab1():
    return f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Лабораторная 1</title>
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center;">

        <h2>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые
        возможности.</h2>

        <nav style="margin-top: 20px;">
            <ul style="list-style-type: none; padding: 0;">
                <li><a href="{url_for('web')}">Веб</a></li>
                <li><a href="{url_for('author')}">Автор</a></li>
                <li><a href="{url_for('image')}">Дуб</a></li>
                <li><a href="{url_for('counter')}">Счётчик</a></li>
                <li><a href="{url_for('info')}">Инфо</a></li>
                <li><a href="{url_for('created')}">Созданный</a></li>
                <li><a href="{url_for('error_400')}">Ошибка 400</a></li>
                <li><a href="{url_for('error_401')}">Ошибка 401</a></li>
                <li><a href="{url_for('error_402')}">Ошибка 402</a></li>
                <li><a href="{url_for('error_403')}">Ошибка 403</a></li>
                <li><a href="/lab1/404">Ошибка 404</a></li>
                <li><a href="{url_for('error_405')}">Ошибка 405</a></li>
                <li><a href="{url_for('error_418')}">Ошибка 418</a></li>
                <li><a href="{url_for('error')}">Ошибка 500</a></li>
            </ul>
        </nav>

        <footer style="margin-top: 40px; font-size: 0.9em; color: gray;">
            <a href="{url_for('index')}">На главную</a>
        </footer>

    </body>
</html>
"""

@app.route('/lab1/400')
def error_400():
    return f"""
    <!doctype html>
    <html>
        <head><title>400 Bad Request</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>400 Bad Request</h1>
            <p>Сервер не может обработать ваш запрос из-за синтаксической ошибки.</p>
        </body>
    </html>
    """, 400

@app.route('/lab1/401')
def error_401():
    return f"""
    <!doctype html>
    <html>
        <head><title>401 Unauthorized</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>401 Unauthorized</h1>
            <p>Необходимо предоставить действительные учетные данные для доступа к этому ресурсу.</p>
        </body>
    </html>
    """, 401

@app.route('/lab1/402')
def error_402():
    return f"""
    <!doctype html>
    <html>
        <head><title>402 Payment Required</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>402 Payment Required</h1>
            <p>Для доступа к ресурсу необходима оплата.</p>
        </body>
    </html>
    """, 402

@app.route('/lab1/403')
def error_403():
    return f"""
    <!doctype html>
    <html>
        <head><title>403 Forbidden</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>403 Forbidden</h1>
            <p>Доступ к ресурсу запрещен. У вас нет прав для выполнения этого действия.</p>
        </body>
    </html>
    """, 403

@app.route('/lab1/405')
def error_405():
    return f"""
    <!doctype html>
    <html>
        <head><title>405 Method Not Allowed</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>405 Method Not Allowed</h1>
            <p>Метод HTTP, который вы использовали, не поддерживается для этого ресурса.</p>
        </body>
    </html>
    """, 405

@app.route('/lab1/418')
def error_418():
    return f"""
    <!doctype html>
    <html>
        <head><title>418 I'm a teapot</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>418 I'm a teapot</h1>
            <p>Я — чайник! Это код ошибки, введенный в апрельскую шутку, RFC 2324.</p>
        </body>
    </html>
    """, 418

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

@app.route('/500')
def error():
    result = 1 / 0  # Деление на ноль, которое вызывает ошибку
    return f"Результат: {result}"

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

@app.route('/lab2/a')
def okey():
    return 'без слэша'

@app.route('/lab2/a/')
def adrenalin():
    return 'со слэшем'