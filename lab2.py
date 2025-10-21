from flask import Blueprint, url_for, request, redirect, Response, render_template, abort
import datetime
lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def okey():
    return 'без слэша'


@lab2.route('/lab2/a/')
def adrenalin():
    return 'со слэшем'

# Словарь цветов и их цен
flowers = {
    'роза': 100,
    'тюльпан': 80,
    'незабудка': 50,
    'ромашка': 60
}


@lab2.route('/lab2/flowers/<int:flower_id>')
def flower_info(flower_id):
    flower_names = list(flowers.keys())
    if not (0 <= flower_id < len(flower_names)):
        abort(404)
    name = flower_names[flower_id]
    price = flowers[name]
    return render_template('lab2/flower_info.html', flower_id=flower_id, name=name, price=price)


@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flowers[name] = price
    return render_template('lab2/flower_added.html', name=name, price=price, total=len(flowers), flower_list=flowers)


@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    abort(400, description="Вы не задали имя цветка")


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flowers.clear()
    return render_template('lab2/flowers_cleared.html')


@lab2.errorhandler(400)
def bad_request(error):
    return render_template('lab2/400.html', description=error.description), 400


@lab2.route('/lab2/flowers_list', methods=['GET', 'POST'])
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
        return redirect(url_for('lab2.flowers_list'))

    return render_template('lab2/flowers_list.html', flowers=flowers)


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    flower_names = list(flowers.keys())
    if not (0 <= flower_id < len(flower_names)):
        abort(404)
    name_to_delete = flower_names[flower_id]
    price = flowers[name_to_delete]
    return render_template('lab2/delete_flower.html', flower_id=flower_id, name=name_to_delete, price=price)


@lab2.route('/lab2/delete_flower_confirm/<int:flower_id>')
def delete_flower_confirm(flower_id):
    flower_names = list(flowers.keys())
    if not (0 <= flower_id < len(flower_names)):
        abort(404)
    name_to_delete = flower_names[flower_id]
    del flowers[name_to_delete]
    return redirect(url_for('lab2.flowers_list'))


@lab2.route('/lab2/example')
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
    return render_template('lab2/example.html', name = name, numer = numer, group = group, cours = cours, fruits = fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "о <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase)


# --- основной роут с двумя параметрами ---
@lab2.route('/lab2/calc/<int:a>/<int:b>')
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
    return render_template('lab2/calc.html', **results)


# --- без параметров ---
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


# --- с одним параметром ---
@lab2.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(url_for('lab2.calc', a=a, b=1))

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


@lab2.route('/lab2/books/')
def show_books():
    return render_template('lab2/books.html', books=books)

# Данные о машинах
cars = [
    {"name": "Toyota Corolla", "image": "lab2/corola.jpg", "description": "Надёжный и экономичный седан для повседневных поездок."},
    {"name": "Honda Civic", "image": "lab2/civic.jpg", "description": "Стильный и динамичный автомобиль с хорошей управляемостью."},
    {"name": "Ford Mustang", "image": "lab2/mustang.jpg", "description": "Американский маслкар с мощным двигателем и агрессивным дизайном."},
    {"name": "Chevrolet Camaro", "image": "lab2/camaro.jpg", "description": "Спортивный автомобиль с ярким и дерзким стилем."},
    {"name": "BMW 3 Series", "image": "lab2/BMW.jpg", "description": "Элегантный немецкий седан с отличной управляемостью."},
    {"name": "Audi A4", "image": "lab2/Audi.jpg", "description": "Комфортный и современный автомобиль с премиальной отделкой."},
    {"name": "Mercedes-Benz C-Class", "image": "lab2/MB.jpg", "description": "Люксовый седан с высоким уровнем комфорта и безопасности."},
    {"name": "Tesla Model 3", "image": "lab2/Tesla.jpg", "description": "Электромобиль с инновационными технологиями и автопилотом."},
    {"name": "Nissan Altima", "image": "lab2/Nissan.jpg", "description": "Практичный седан с хорошей экономией топлива и просторным салоном."},
    {"name": "Hyundai Elantra", "image": "lab2/Hundai.jpg", "description": "Доступный и надёжный автомобиль для ежедневных поездок."},
    {"name": "Volkswagen Golf", "image": "lab2/Golf.jpg", "description": "Компактный хэтчбек с удобным управлением и современным дизайном."},
    {"name": "Subaru Impreza", "image": "lab2/Subaru.jpg", "description": "Надёжный автомобиль с полным приводом для любых дорог."},
    {"name": "Mazda CX-5", "image": "lab2/Mazda.jpg", "description": "Стильный кроссовер с отличной управляемостью и комфортом."},
    {"name": "Jeep Wrangler", "image": "lab2/Jeep.jpg", "description": "Легендарный внедорожник для приключений на любой местности."},
    {"name": "Porsche 911", "image": "lab2/Porsche.jpg", "description": "Икона спортивных автомобилей с невероятной динамикой."},
    {"name": "Lamborghini Huracan", "image": "lab2/Lambo.jpg", "description": "Экзотический суперкар с уникальным дизайном и мощью."},
    {"name": "Ferrari F8", "image": "lab2/Ferrari.jpg", "description": "Высокопроизводительный суперкар с изысканным стилем."},
    {"name": "Bugatti Chiron", "image": "lab2/Buga.jpg", "description": "Сверхскоростной гиперкар для настоящих энтузиастов."},
    {"name": "Kia Sorento", "image": "lab2/kia.jpg", "description": "Просторный семейный SUV с современными технологиями."},
    {"name": "Renault Clio", "image": "lab2/Clio.jpg", "description": "Компактный и экономичный хэтчбек для города."},
]


@lab2.route("/lab2/cars/")
def show_cars():
    return render_template("lab2/cars.html", cars=cars)