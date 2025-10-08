from flask import Flask, url_for, request, redirect, render_template, Response, abort
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
    return render_template('index.html')


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

# Словарь цветов и их цен
flowers = {
    'роза': 100,
    'тюльпан': 80,
    'незабудка': 50,
    'ромашка': 60
}

@app.route('/lab2/flowers/<int:flower_id>')
def flower_info(flower_id):
    flower_names = list(flowers.keys())
    if not (0 <= flower_id < len(flower_names)):
        abort(404)
    name = flower_names[flower_id]
    price = flowers[name]
    return render_template('flower_info.html', flower_id=flower_id, name=name, price=price)


@app.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flowers[name] = price
    return render_template('flower_added.html', name=name, price=price, total=len(flowers), flower_list=flowers)


@app.route('/lab2/add_flower/')
def add_flower_empty():
    abort(400, description="Вы не задали имя цветка")


@app.route('/lab2/clear_flowers')
def clear_flowers():
    flowers.clear()
    return render_template('flowers_cleared.html')


@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html', description=error.description), 400


@app.route('/lab2/flowers_list', methods=['GET', 'POST'])
def flowers_list():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if not name or not price:
            abort(400, description="Название или цена не заданы")
        try:
            price = int(price)
        except ValueError:
            abort(400, description="Цена должна быть числом")
        flowers[name] = price
        return redirect(url_for('flowers_list'))

    return render_template('flowers_list.html', flowers=flowers)
    
@app.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    flower_names = list(flowers.keys())
    if flower_id >= len(flower_names):
        abort(404)
    name_to_delete = flower_names[flower_id]
    price = flowers[name_to_delete]
    return render_template('delete_flower.html', flower_id=flower_id, name=name_to_delete, price=price)

@app.route('/lab2/delete_flower_confirm/<int:flower_id>')
def delete_flower_confirm(flower_id):
    flower_names = list(flowers.keys())
    if flower_id >= len(flower_names):
        abort(404)
    name_to_delete = flower_names[flower_id]
    del flowers[name_to_delete]
    return redirect(url_for('flowers_list'))

@app.route('/lab2/example')
def example():
    name = 'Богданов Семён'
    numer = '2'
    group = 'ФБИ-32'
    cours = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name = name, numer = numer, group = group, cours = cours, fruits = fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "о <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

# --- основной роут с двумя параметрами ---
@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    results = {
        'a': a,
        'b': b,
        'sum': a + b,
        'sub': a - b,
        'mul': a * b,
        'div': a / b if b != 0 else 'нельзя делить на 0',
        'pow': a ** b
    }
    return render_template('calc.html', **results)


# --- без параметров ---
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))


# --- с одним параметром ---
@app.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(url_for('calc', a=a, b=1))

# список книг
books = [
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 672},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Исторический роман", "pages": 1225},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 320},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Мистика", "pages": 480},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Сатира", "pages": 352},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 280},
    {"author": "Антон Чехов", "title": "Вишнёвый сад", "genre": "Пьеса", "pages": 160},
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Фантастика", "pages": 256},
    {"author": "Дж. Р. Р. Толкин", "title": "Хоббит", "genre": "Фэнтези", "pages": 310}
]

@app.route('/lab2/books/')
def show_books():
    return render_template('books.html', books=books)

# Данные о машинах
cars = [
    {"name": "Toyota Corolla", "image": "corola.jpg", "description": "Надёжный и экономичный седан для повседневных поездок."},
    {"name": "Honda Civic", "image": "civic.jpg", "description": "Стильный и динамичный автомобиль с хорошей управляемостью."},
    {"name": "Ford Mustang", "image": "mustang.jpg", "description": "Американский маслкар с мощным двигателем и агрессивным дизайном."},
    {"name": "Chevrolet Camaro", "image": "camaro.jpg", "description": "Спортивный автомобиль с ярким и дерзким стилем."},
    {"name": "BMW 3 Series", "image": "BMW.jpg", "description": "Элегантный немецкий седан с отличной управляемостью."},
    {"name": "Audi A4", "image": "Audi.jpg", "description": "Комфортный и современный автомобиль с премиальной отделкой."},
    {"name": "Mercedes-Benz C-Class", "image": "MB.jpg", "description": "Люксовый седан с высоким уровнем комфорта и безопасности."},
    {"name": "Tesla Model 3", "image": "Tesla.jpg", "description": "Электромобиль с инновационными технологиями и автопилотом."},
    {"name": "Nissan Altima", "image": "Nissan.jpg", "description": "Практичный седан с хорошей экономией топлива и просторным салоном."},
    {"name": "Hyundai Elantra", "image": "Hundai.jpg", "description": "Доступный и надёжный автомобиль для ежедневных поездок."},
    {"name": "Volkswagen Golf", "image": "Golf.jpg", "description": "Компактный хэтчбек с удобным управлением и современным дизайном."},
    {"name": "Subaru Impreza", "image": "Subaru.jpg", "description": "Надёжный автомобиль с полным приводом для любых дорог."},
    {"name": "Mazda CX-5", "image": "Mazda.jpg", "description": "Стильный кроссовер с отличной управляемостью и комфортом."},
    {"name": "Jeep Wrangler", "image": "Jeep.jpg", "description": "Легендарный внедорожник для приключений на любой местности."},
    {"name": "Porsche 911", "image": "Porsche.jpg", "description": "Икона спортивных автомобилей с невероятной динамикой."},
    {"name": "Lamborghini Huracan", "image": "Lambo.jpg", "description": "Экзотический суперкар с уникальным дизайном и мощью."},
    {"name": "Ferrari F8", "image": "Ferrari.jpg", "description": "Высокопроизводительный суперкар с изысканным стилем."},
    {"name": "Bugatti Chiron", "image": "Buga.jpg", "description": "Сверхскоростной гиперкар для настоящих энтузиастов."},
    {"name": "Kia Sorento", "image": "kia.jpg", "description": "Просторный семейный SUV с современными технологиями."},
    {"name": "Renault Clio", "image": "Clio.jpg", "description": "Компактный и экономичный хэтчбек для города."},
]

@app.route("/lab2/cars/")
def show_cars():
    return render_template("cars.html", cars=cars)