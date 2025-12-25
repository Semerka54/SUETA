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
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'full_name')

    query = Employee.query

    if search:
        query = query.filter(
            Employee.full_name.ilike(f'%{search}%') |
            Employee.position.ilike(f'%{search}%') |
            Employee.gender.ilike(f'%{search}%') |
            Employee.phone.ilike(f'%{search}%') |
            Employee.email.ilike(f'%{search}%')
        )

    if hasattr(Employee, sort):
        query = query.order_by(getattr(Employee, sort))

    employees = query.paginate(page=page, per_page=20)

    return render_template(
        'rgz/employees.html',
        employees=employees,
        student=STUDENT
    )


# ===== ДОБАВЛЕНИЕ СОТРУДНИКА =====

@rgz.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        data = request.form

        if not (
            validate_text(data.get('full_name')) and
            validate_text(data.get('position')) and
            validate_gender(data.get('gender')) and
            validate_phone(data.get('phone')) and
            validate_email(data.get('email'))
        ):
            return "Невалидные данные", 400

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
        return redirect(url_for('rgz.employees'))

    return render_template('rgz/employee_form.html', student=STUDENT)


# ===== РЕДАКТИРОВАНИЕ СОТРУДНИКА =====

@rgz.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    emp = Employee.query.get_or_404(id)

    if request.method == 'POST':
        data = request.form

        if not (
            validate_text(data.get('full_name')) and
            validate_text(data.get('position')) and
            validate_gender(data.get('gender')) and
            validate_phone(data.get('phone')) and
            validate_email(data.get('email'))
        ):
            return "Невалидные данные", 400

        emp.full_name = data['full_name']
        emp.position = data['position']
        emp.gender = data['gender']
        emp.phone = data['phone']
        emp.email = data['email']
        emp.probation = 'probation' in data
        emp.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d')

        db_rgz.session.commit()
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
