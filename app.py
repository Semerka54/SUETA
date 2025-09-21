from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы", 404

@app.route("/web")
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

@app.route("/author")
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
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route('/image')
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

@app.route('/counter')
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
        <a href="/counter/reset">Сбросить счётчик</a>
    </body>
</html>
'''

@app.route('/counter/reset')
def counter_reset():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        Счётчик обнулён.<br>
        <a href="/counter">Назад к счётчику</a>
    </body>
</html>
'''

@app.route('/info')
def info():
    return redirect("author")

@app.route("/created")
def created():
    return """
    <!doctype html>
    <html>
        <body>
            <h1>web-сервер на flask</h1>
            <a href="/author">author</a>
        </body>
    </html>
    """, 201