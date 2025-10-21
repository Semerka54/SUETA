from flask import Blueprint, url_for, request, redirect, Response
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/html; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Богданов Семён Андреевич"
    group = "ФБИ-32"
    faculty = "ФБ"

    return f"""<!doctype html>
        <html>
            <body>
                <p>Студент: {name}</p>
                <p>Группа: {group}</p>
                <p>Факультет: {faculty}</p>
                <a href="{url_for('lab1.web')}">web</a>
            </body>
        </html>"""


@lab1.route('/lab1/image')
def image():
    img_path = url_for("static", filename="lab1/dub.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
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


@lab1.route('/lab1/counter')
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
        <a href="{url_for('lab1.counter_reset')}">Сбросить счётчик</a>
    </body>
</html>
'''


@lab1.route('/lab1/counter/reset')
def counter_reset():
    global count
    count = 0
    return f'''
<!doctype html>
<html>
    <body>
        Счётчик обнулён.<br>
        <a href="{url_for('lab1.counter')}">Назад к счётчику</a>
    </body>
</html>
'''


@lab1.route('/lab1/info')
def info():
    return redirect(url_for('lab1.author'))


@lab1.route("/lab1/created")
def created():
    return f"""
    <!doctype html>
    <html>
        <body>
            <h1>web-сервер на flask</h1>
            <a href="{url_for('lab1.author')}">author</a>
        </body>
    </html>
    """, 201


@lab1.route('/lab1')
def lab():
    return f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Лабораторная 1</title>
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center;">

        <h2>Flask — фреймворк для создания веб-приложений на Python, использующий Werkzeug и Jinja2.</h2>

        <nav style="margin-top: 20px;">
            <ul style="list-style-type: none; padding: 0;">
                <li><a href="{url_for('lab1.web')}">Веб</a></li>
                <li><a href="{url_for('lab1.author')}">Автор</a></li>
                <li><a href="{url_for('lab1.image')}">Дуб</a></li>
                <li><a href="{url_for('lab1.counter')}">Счётчик</a></li>
                <li><a href="{url_for('lab1.info')}">Инфо</a></li>
                <li><a href="{url_for('lab1.created')}">Созданный</a></li>
                <li><a href="{url_for('lab1.error_400')}">Ошибка 400</a></li>
                <li><a href="{url_for('lab1.error_401')}">Ошибка 401</a></li>
                <li><a href="{url_for('lab1.error_402')}">Ошибка 402</a></li>
                <li><a href="{url_for('lab1.error_403')}">Ошибка 403</a></li>
                <li><a href="/lab1/404">Ошибка 404</a></li>
                <li><a href="{url_for('lab1.error_405')}">Ошибка 405</a></li>
                <li><a href="{url_for('lab1.error_418')}">Ошибка 418</a></li>
                <li><a href="{url_for('lab1.error')}">Ошибка 500</a></li>
            </ul>
        </nav>

        <footer style="margin-top: 40px; font-size: 0.9em; color: gray;">
            <a href="/">На главную</a>
        </footer>
    </body>
</html>
"""


@lab1.route('/lab1/400')
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


@lab1.route('/lab1/401')
def error_401():
    return f"""
    <!doctype html>
    <html>
        <head><title>401 Unauthorized</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>401 Unauthorized</h1>
            <p>Необходимо предоставить действительные учетные данные.</p>
        </body>
    </html>
    """, 401


@lab1.route('/lab1/402')
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


@lab1.route('/lab1/403')
def error_403():
    return f"""
    <!doctype html>
    <html>
        <head><title>403 Forbidden</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>403 Forbidden</h1>
            <p>Доступ к ресурсу запрещён.</p>
        </body>
    </html>
    """, 403


@lab1.route('/lab1/405')
def error_405():
    return f"""
    <!doctype html>
    <html>
        <head><title>405 Method Not Allowed</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>405 Method Not Allowed</h1>
            <p>Метод HTTP не поддерживается для этого ресурса.</p>
        </body>
    </html>
    """, 405


@lab1.route('/lab1/418')
def error_418():
    return f"""
    <!doctype html>
    <html>
        <head><title>418 I'm a teapot</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>418 I'm a teapot</h1>
            <p>Я — чайник! RFC 2324.</p>
        </body>
    </html>
    """, 418


@lab1.route('/lab1/500')
def error():
    result = 1 / 0  # специально вызывает ошибку
    return f"Результат: {result}"