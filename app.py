from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы", 404

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
    return f'''
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
            </ul>
        </nav>

        <footer style="margin-top: 40px; font-size: 0.9em; color: gray;">
            <a href="{url_for('index')}">На главную</a>
        </footer>

    </body>
</html>
"""