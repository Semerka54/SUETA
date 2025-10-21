from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session
import datetime
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    # Обработка значений по умолчанию
    if name is None:
        name = "Аноним"
    if age is None:
        age = "неизвестно"
    
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user', '').strip()
    age  = request.args.get('age', '').strip()
    sex  = request.args.get('sex', 'male')

    errors = {}

    if 'user' in request.args or 'age' in request.args:
        if not user:
            errors['user'] = 'Заполните поле!'
        if not age:
            errors['age'] = 'Заполните поле!'
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)   


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай – 80 рублей, зелёный – 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара – на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    if color or bg_color or font_size or font_style:
        resp = make_response(redirect(url_for('lab3.settings')))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    # Загружаем сохранённые настройки
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    font_style = request.cookies.get('font_style', 'normal')

    return render_template('lab3/settings.html',
                           color=color,
                           bg_color=bg_color,
                           font_size=font_size,
                           font_style=font_style)


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        # Получаем данные из формы
        fio = request.form['fio']
        shelf = request.form['shelf']
        linen = 'linen' in request.form  # Преобразуем checkbox в булевое значение
        luggage = 'luggage' in request.form
        age = int(request.form['age'])
        departure = request.form['departure']
        destination = request.form['destination']
        date = request.form['date']
        insurance = 'insurance' in request.form

        # Проверка на пустые поля и возраст
        if not fio or not shelf or not age or not departure or not destination or not date:
            return "Все поля должны быть заполнены!", 400
        
        if age < 1 or age > 120:
            return "Возраст должен быть от 1 до 120 лет", 400

        # Расчёт стоимости билета
        if age < 18:
            price = 700  # Детский билет
            ticket_type = "Детский билет"
        else:
            price = 1000  # Взрослый билет
            ticket_type = "Взрослый билет"

        # Дополнительные стоимости
        shelf_price = 0
        if shelf in ['нижняя', 'нижняя боковая']:
            shelf_price = 100
            price += shelf_price

        linen_price = 75 if linen else 0
        price += linen_price

        luggage_price = 250 if luggage else 0
        price += luggage_price

        insurance_price = 150 if insurance else 0
        price += insurance_price

        # Сохраняем данные в сессии
        session['ticket_data'] = {
            'fio': fio,
            'shelf': shelf,
            'linen': linen,
            'luggage': luggage,
            'age': age,
            'departure': departure,
            'destination': destination,
            'date': date,
            'insurance': insurance,
            'ticket_type': ticket_type,
            'price': price,
            'shelf_price': shelf_price,
            'linen_price': linen_price,
            'luggage_price': luggage_price,
            'insurance_price': insurance_price
        }

        # Перенаправление на страницу с билетом
        return redirect(url_for('lab3.ticket_details'))

    return render_template('lab3/form2.html')



@lab3.route('/lab3/ticket_details')
def ticket_details():
    # Получаем данные из сессии
    ticket_data = session.get('ticket_data', None)

    if ticket_data is None:
        return "Ошибка: Данные о билете не найдены!", 400

    # Отображаем страницу с билетом
    return render_template('lab3/ticket_form.html', **ticket_data)



@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect(url_for('lab3.settings')))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_style')
    return resp


# Список автомобилей: марка, модель, цена, цвет, тип кузова
cars_list = [
    {"brand": "Toyota", "model": "Corolla", "price": 20000, "equipment": "Standard", "body_type": "Sedan"},
    {"brand": "Honda", "model": "Civic", "price": 25000, "equipment": "Luxury", "body_type": "Sedan"},
    {"brand": "BMW", "model": "3 Series", "price": 35000, "equipment": "Sport", "body_type": "Sedan"},
    {"brand": "Mercedes", "model": "C-Class", "price": 40000, "equipment": "Premium", "body_type": "Sedan"},
    {"brand": "Audi", "model": "A4", "price": 38000, "equipment": "Executive", "body_type": "Sedan"},
    {"brand": "Ford", "model": "Focus", "price": 18000, "equipment": "Standard", "body_type": "Hatchback"},
    {"brand": "Chevrolet", "model": "Malibu", "price": 22000, "equipment": "Luxury", "body_type": "Sedan"},
    {"brand": "Volkswagen", "model": "Golf", "price": 24000, "equipment": "Sport", "body_type": "Hatchback"},
    {"brand": "Nissan", "model": "Altima", "price": 27000, "equipment": "Premium", "body_type": "Sedan"},
    {"brand": "Mazda", "model": "Mazda3", "price": 26000, "equipment": "Standard", "body_type": "Hatchback"},
    {"brand": "Tesla", "model": "Model 3", "price": 45000, "equipment": "Luxury", "body_type": "Sedan"},
    {"brand": "Lexus", "model": "IS", "price": 46000, "equipment": "Executive", "body_type": "Sedan"},
    {"brand": "Jaguar", "model": "XE", "price": 42000, "equipment": "Sport", "body_type": "Sedan"},
    {"brand": "Hyundai", "model": "Elantra", "price": 19000, "equipment": "Standard", "body_type": "Sedan"},
    {"brand": "Kia", "model": "Forte", "price": 21000, "equipment": "Luxury", "body_type": "Sedan"},
    {"brand": "Subaru", "model": "Impreza", "price": 23000, "equipment": "Premium", "body_type": "Hatchback"},
    {"brand": "Peugeot", "model": "308", "price": 22000, "equipment": "Standard", "body_type": "Hatchback"},
    {"brand": "Ford", "model": "Mustang", "price": 50000, "equipment": "Sport", "body_type": "Coupe"},
    {"brand": "Chevrolet", "model": "Camaro", "price": 55000, "equipment": "Luxury", "body_type": "Coupe"},
    {"brand": "Porsche", "model": "911", "price": 90000, "equipment": "Premium", "body_type": "Coupe"},
]


@lab3.route("/lab3/cars", methods=["GET", "POST"])
def cars_page():
    # Получаем куки с минимальной и максимальной ценой
    min_price = request.cookies.get("min_price", default=0, type=int)
    max_price = request.cookies.get("max_price", default=100000, type=int)

    # Получаем выбранные параметры из куки или формы
    body_type_selected = request.cookies.get("body_type", default=None)
    equipment_selected = request.cookies.get("equipment", default=None)
    brand_selected = request.cookies.get("brand", default=None)

    if request.method == "POST":
        # Получаем значения из формы
        min_price_input = request.form.get("min_price")
        max_price_input = request.form.get("max_price")
        body_type_input = request.form.get("body_type")
        equipment_input = request.form.get("equipment")
        brand_input = request.form.get("brand")

        # Проверяем, если одно из полей пустое, то не фильтруем по этому полю
        if min_price_input and max_price_input:
            try:
                min_price_input = int(min_price_input)
                max_price_input = int(max_price_input)
                if min_price_input > max_price_input:
                    # Автоматически меняем местами минимальную и максимальную цену
                    min_price_input, max_price_input = max_price_input, min_price_input
            except ValueError:
                pass
        else:
            if min_price_input:
                min_price_input = int(min_price_input)
            if max_price_input:
                max_price_input = int(max_price_input)

        # Фильтрация машин по параметрам
        filtered_cars = filter_cars(min_price_input, max_price_input, body_type_input, equipment_input, brand_input)

        # Сохраняем значения в куки
        resp = make_response(render_template(
            "lab3/cars_results.html", 
            cars=filtered_cars,
            min_price=min_price_input, 
            max_price=max_price_input,
            total_count=len(filtered_cars), 
            body_types=get_unique_values("body_type"),
            equipments=get_unique_values("equipment"),  # Передаем комплектации
            brands=get_unique_values("brand"),
            body_type_selected=body_type_input,  # Передаем выбранные параметры в шаблон
            equipment_selected=equipment_input,
            brand_selected=brand_input
        ))
        resp.set_cookie("min_price", str(min_price_input))
        resp.set_cookie("max_price", str(max_price_input))
        resp.set_cookie("body_type", body_type_input or "")  # Сохраняем выбор кузова
        resp.set_cookie("equipment", equipment_input or "")  # Сохраняем выбор комплектации
        resp.set_cookie("brand", brand_input or "")  # Сохраняем выбор бренда
        return resp

    return render_template(
        "lab3/cars_results.html", 
        cars=filter_cars(min_price, max_price), 
        min_price=min_price, 
        max_price=max_price,
        total_count=len(filter_cars(min_price, max_price)), 
        body_types=get_unique_values("body_type"),
        equipments=get_unique_values("equipment"),  # Передаем комплектации
        brands=get_unique_values("brand"),
        body_type_selected=body_type_selected,  # Передаем выбранные параметры в шаблон
        equipment_selected=equipment_selected,
        brand_selected=brand_selected
    )


def filter_cars(min_price, max_price, body_type=None, equipment=None, brand=None):
    # Фильтрация машин по цене и дополнительным параметрам
    filtered = [
        car for car in cars_list if min_price <= car["price"] <= max_price and
        (not body_type or car["body_type"].lower() == body_type.lower()) and
        (not equipment or car["equipment"].lower() == equipment.lower()) and
        (not brand or car["brand"].lower() == brand.lower())
    ]
    return filtered


def get_unique_values(attribute):
    # Получение уникальных значений для каждого параметра
    return list(set([car[attribute] for car in cars_list]))


@lab3.route("/lab3/reset")
def reset():
    # Очистка куки
    resp = make_response(redirect(url_for("lab3.cars_page")))
    resp.delete_cookie("min_price")
    resp.delete_cookie("max_price")
    resp.delete_cookie("body_type")
    resp.delete_cookie("equipment")
    resp.delete_cookie("brand")
    return resp

