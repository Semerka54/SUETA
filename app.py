from flask import Flask, url_for, request, redirect, render_template, Response, abort
import datetime
from lab1 import lab1
app = Flask(__name__)
app.register_blueprint(lab1)

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
    if not (0 <= flower_id < len(flower_names)):
        abort(404)
    name_to_delete = flower_names[flower_id]
    price = flowers[name_to_delete]
    return render_template('delete_flower.html', flower_id=flower_id, name=name_to_delete, price=price)

@app.route('/lab2/delete_flower_confirm/<int:flower_id>')
def delete_flower_confirm(flower_id):
    flower_names = list(flowers.keys())
    if not (0 <= flower_id < len(flower_names)):
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