from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session
from functools import wraps
import datetime
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x2 == 0:
        return render_template('lab4/div.html', error='Ошибка: деление на ноль невозможно!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


# Суммирование
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


# Умножение
@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


# Вычитание
@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


# Возведение в степень
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Ошибка: оба числа не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:  # Проверка, чтобы счетчик не ушел в отрицательную область
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < 10:  # Проверка, чтобы не посадить больше 10 деревьев
            tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Иванов', 'gender': 'male'},
    {'login': 'maria', 'password': '789', 'name': 'Мария Сидорова', 'gender': 'female'},
    {'login': 'john', 'password': 'abc', 'name': 'John Smith', 'gender': 'male'},
    {'login': 'sarah', 'password': 'qwerty', 'name': 'Sarah Johnson', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_login = session['login']
            # Находим пользователя для отображения имени
            user_data = next((user for user in users if user['login'] == user_login), None)
            user_name = user_data['name'] if user_data else user_login
        else:
            authorized = False
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, user_name=user_name)

    login_input = request.form.get('login')
    password = request.form.get('password')
    
    # Проверяем, что оба поля заполнены
    if not login_input:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login_input=login_input)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login_input=login_input)
    
    # Ищем пользователя в списке
    for user in users:
        if login_input == user['login'] and password == user['password']:
            session['login'] = login_input
            session['user_name'] = user['name']  # Сохраняем имя в сессии
            return redirect('/lab4/login')
    
    # Если пользователь не найден
    error = 'Неверные логин или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login_input=login_input)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('user_name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = request.form.get('temperature')
    message = ''
    snowflakes = 0
    error = ''
    
    if request.method == 'POST':
        if not temperature:
            error = 'Ошибка: не задана температура'
        else:
            try:
                temp = float(temperature)
                if temp < -12:
                    error = 'Не удалось установить температуру — слишком низкое значение'
                elif temp > -1:
                    error = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temp <= -9:
                    message = f'Установлена температура: {temp}°C'
                    snowflakes = 3
                elif -8 <= temp <= -5:
                    message = f'Установлена температура: {temp}°C'
                    snowflakes = 2
                elif -4 <= temp <= -1:
                    message = f'Установлена температура: {temp}°C'
                    snowflakes = 1
            except ValueError:
                error = 'Ошибка: введите числовое значение температуры'
    
    return render_template('lab4/fridge.html', 
                         message=message, 
                         error=error, 
                         snowflakes=snowflakes,
                         temperature=temperature or '')


@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    grain_types = {
        'barley': {'name': 'ячмень', 'price': 12000},
        'oats': {'name': 'овёс', 'price': 8500},
        'wheat': {'name': 'пшеница', 'price': 9000},
        'rye': {'name': 'рожь', 'price': 15000}
    }
    
    grain = request.form.get('grain')
    weight = request.form.get('weight')
    message = ''
    error = ''
    discount_applied = False
    discount_amount = 0
    total_amount = 0
    
    if request.method == 'POST':
        if not grain:
            error = 'Ошибка: выберите тип зерна'
        elif not weight:
            error = 'Ошибка: не указан вес'
        else:
            try:
                weight_float = float(weight)
                if weight_float <= 0:
                    error = 'Ошибка: вес должен быть больше 0'
                elif weight_float > 100:
                    error = 'Извините, такого объёма сейчас нет в наличии'
                else:
                    # Расчет стоимости
                    grain_data = grain_types[grain]
                    base_price = grain_data['price']
                    total_amount = weight_float * base_price
                    
                    # Применение скидки
                    if weight_float > 10:
                        discount_amount = total_amount * 0.1
                        total_amount -= discount_amount
                        discount_applied = True
                    
                    # Форматирование чисел с разделителями тысяч
                    formatted_total = "{:,.0f}".format(total_amount).replace(",", " ")
                    message = f'Заказ успешно сформирован. Вы заказали {grain_data["name"]}. Вес: {weight_float} т. Сумма к оплате: {formatted_total} руб'
                    
            except ValueError:
                error = 'Ошибка: введите корректное числовое значение веса'
    
    return render_template('lab4/grain_order.html', 
                         message=message, 
                         error=error, 
                         grain_types=grain_types,
                         grain=grain or '',
                         weight=weight or '',
                         discount_applied=discount_applied,
                         discount_amount=discount_amount,
                         total_amount=total_amount)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            return redirect('/lab4/login')
        return f(*args, **kwargs)
    return decorated_function


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    
    # Проверки
    if not login or not password or not password_confirm or not name:
        error = 'Заполните все поля'
        return render_template('lab4/register.html', error=error, login=login, name=name)
    
    if password != password_confirm:
        error = 'Пароли не совпадают'
        return render_template('lab4/register.html', error=error, login=login, name=name)
    
    # Проверка на существующий логин
    for user in users:
        if user['login'] == login:
            error = 'Пользователь с таким логином уже существует'
            return render_template('lab4/register.html', error=error, login=login, name=name)
    
    # Добавление нового пользователя
    new_user = {
        'login': login,
        'password': password,
        'name': name
    }
    users.append(new_user)
    
    # Автоматическая авторизация после регистрации
    session['login'] = login
    session['user_name'] = name
    
    return redirect('/lab4/login')


@lab4.route('/lab4/users')
@login_required
def users_list():
    # Создаем копию списка пользователей без паролей для безопасности
    users_safe = []
    for user in users:
        users_safe.append({
            'login': user['login'],
            'name': user['name']
        })
    
    current_user_login = session['login']
    return render_template('lab4/users.html', 
                         users=users_safe, 
                         current_user=current_user_login)


@lab4.route('/lab4/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    if request.method == 'GET':
        return render_template('lab4/confirm_delete.html')  # Страница подтверждения
    
    current_user = session['login']
    print(f"Попытка удаления пользователя: {current_user}")
    
    # Находим и удаляем пользователя
    for i, user in enumerate(users):
        if user['login'] == current_user:
            users.pop(i)
            print(f"Пользователь {current_user} удален")
            # Выход после удаления
            session.pop('login', None)
            session.pop('user_name', None)
            return redirect('/lab4/login')
    
    print(f"Пользователь {current_user} не найден")
    return redirect('/lab4/users')


@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    current_user_login = session['login']
    current_user = None
    
    # Находим текущего пользователя
    for user in users:
        if user['login'] == current_user_login:
            current_user = user
            break
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', 
                             user=current_user, 
                             error='')
    
    # Обработка POST запроса
    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    
    # Проверки
    if not new_login or not new_name:
        error = 'Логин и имя обязательны для заполнения'
        return render_template('lab4/edit_user.html', 
                             user=current_user, 
                             error=error)
    
    # Проверка на уникальность логина (если изменился)
    if new_login != current_user_login:
        for user in users:
            if user['login'] == new_login:
                error = 'Пользователь с таким логином уже существует'
                return render_template('lab4/edit_user.html', 
                                     user=current_user, 
                                     error=error)
    
    # Проверка пароля
    if new_password:
        if new_password != password_confirm:
            error = 'Пароли не совпадают'
            return render_template('lab4/edit_user.html', 
                                 user=current_user, 
                                 error=error)
    
    # Обновление данных
    current_user['login'] = new_login
    current_user['name'] = new_name
    if new_password:  # Обновляем пароль только если он указан
        current_user['password'] = new_password
    
    # Обновляем сессию
    session['login'] = new_login
    session['user_name'] = new_name
    
    return redirect('/lab4/users')