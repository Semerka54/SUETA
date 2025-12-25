from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user
from datetime import datetime
from .models import Employee, Admin
from .db_rgz import db_rgz
import re

rgz = Blueprint(
    'rgz',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/rgz'
)

STUDENT = "Богданов Семён Андреевич, ФБИ-32"


# ===== ВАЛИДАЦИЯ =====

def validate_text(text):
    return bool(text and text.strip())


def validate_gender(gender):
    return gender in ('М', 'Ж')


def validate_phone(phone):
    return bool(re.match(r'^[0-9()+\- ]+$', phone))


def validate_email(email):
    return bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', email))


# ===== АВТОРИЗАЦИЯ =====

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('rgz.employees'))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('rgz.employees'))
        else:
            flash("Неверный логин или пароль")

    return render_template('rgz/login.html', student=STUDENT)


@rgz.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('rgz.login'))


@rgz.route('/delete_account')
@login_required
def delete_account():
    db_rgz.session.delete(current_user)
    db_rgz.session.commit()
    logout_user()
    return redirect(url_for('rgz.login'))


# ===== СПИСОК СОТРУДНИКОВ =====

@rgz.route('/employees')
def employees():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'full_name')
    
    query = Employee.query
    
    if search:
        # Пробуем распознать дату
        from datetime import datetime
        
        # Форматы дат для распознавания
        date_formats = [
            '%Y-%m-%d',      # 2023-10-15
            '%d.%m.%Y',      # 15.10.2023
            '%d.%m.%y',      # 15.10.23
            '%d/%m/%Y',      # 15/10/2023
            '%d/%m/%y',      # 15/10/23
            '%d-%m-%Y',      # 15-10-2023
            '%d-%m-%y',      # 15-10-23
            '%Y.%m.%d',      # 2023.10.15
            '%Y/%m/%d',      # 2023/10/15
        ]
        
        date_search = None
        search_is_date = False
        
        # Пробуем каждый формат даты
        for fmt in date_formats:
            try:
                date_search = datetime.strptime(search, fmt).date()
                search_is_date = True
                break
            except ValueError:
                continue
        
        # Если введена дата, ищем по дате приёма
        if search_is_date and date_search:
            from sqlalchemy import cast, String
            query = query.filter(
                cast(Employee.hire_date, String).ilike(f'%{date_search}%')
            )
        else:
            # Если это не дата, ищем по всем текстовым полям
            from sqlalchemy import or_, cast, String
            search_terms = search.split()
            conditions = []
            for term in search_terms:
                term = f'%{term}%'
                conditions.extend([
                    Employee.full_name.ilike(term),
                    Employee.position.ilike(term),
                    Employee.gender.ilike(term),
                    Employee.phone.ilike(term),
                    Employee.email.ilike(term),
                    # Добавляем поиск по дате в текстовом виде
                    cast(Employee.hire_date, String).ilike(f'%{term}%'),
                ])
            
            query = query.filter(or_(*conditions))
    
    # Сортировка
    valid_sort_fields = ['full_name', 'position', 'gender', 'phone', 'email', 'hire_date']
    if sort in valid_sort_fields:
        query = query.order_by(getattr(Employee, sort))
    else:
        query = query.order_by(Employee.full_name)
    
    employees = query.paginate(page=page, per_page=20)
    
    return render_template(
        'rgz/employees.html',
        employees=employees,
        student=STUDENT,
        current_search=search,
        current_sort=sort
    )
# ===== ДОБАВЛЕНИЕ СОТРУДНИКА =====

@rgz.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        data = request.form
        
        # Детальная проверка с сообщениями
        errors = []
        
        if not validate_text(data.get('full_name')):
            errors.append('ФИО обязательно для заполнения')
        
        if not validate_text(data.get('position')):
            errors.append('Должность обязательна для заполнения')
        
        if not validate_gender(data.get('gender')):
            errors.append('Пол должен быть "М" или "Ж"')
        
        if not validate_phone(data.get('phone')):
            errors.append('Некорректный номер телефона')
        
        if not validate_email(data.get('email')):
            errors.append('Некорректный email адрес')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('rgz.add_employee'))
        
        emp = Employee(
            full_name=data['full_name'],
            position=data['position'],
            gender=data['gender'],
            phone=data['phone'],
            email=data['email'],
            probation='probation' in data,
            hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d')
        )
        
        db_rgz.session.add(emp)
        db_rgz.session.commit()
        flash('✅ Сотрудник успешно добавлен!', 'success')
        return redirect(url_for('rgz.employees'))
    
    return render_template('rgz/employee_form.html', student=STUDENT)


# ===== РЕДАКТИРОВАНИЕ СОТРУДНИКА =====

@rgz.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    emp = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        data = request.form
        
        errors = []
        
        if not validate_text(data.get('full_name')):
            errors.append('ФИО обязательно для заполнения')
        
        if not validate_text(data.get('position')):
            errors.append('Должность обязательна для заполнения')
        
        if not validate_gender(data.get('gender')):
            errors.append('Пол должен быть "М" или "Ж"')
        
        if not validate_phone(data.get('phone')):
            errors.append('Некорректный номер телефона')
        
        if not validate_email(data.get('email')):
            errors.append('Некорректный email адрес')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template(
                'rgz/employee_form.html',
                employee=emp,
                student=STUDENT
            )
        
        emp.full_name = data['full_name']
        emp.position = data['position']
        emp.gender = data['gender']
        emp.phone = data['phone']
        emp.email = data['email']
        emp.probation = 'probation' in data
        emp.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d')
        
        db_rgz.session.commit()
        flash('✅ Данные сотрудника обновлены!', 'success')
        return redirect(url_for('rgz.employees'))
    
    return render_template(
        'rgz/employee_form.html',
        employee=emp,
        student=STUDENT
    )


# ===== УДАЛЕНИЕ СОТРУДНИКА =====

@rgz.route('/delete/<int:id>')
@login_required
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    db_rgz.session.delete(emp)
    db_rgz.session.commit()
    return redirect(url_for('rgz.employees'))
