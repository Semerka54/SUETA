from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import Employee
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


def validate_text(text):
    return bool(re.match(r'^[A-Za-zА-Яа-я0-9 .\-@]+$', text))


@rgz.route('/employees')
def employees():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'full_name')

    query = Employee.query

    if search:
        query = query.filter(
            (Employee.full_name.ilike(f'%{search}%')) |
            (Employee.position.ilike(f'%{search}%')) |
            (Employee.gender.ilike(f'%{search}%')) |
            (Employee.phone.ilike(f'%{search}%')) |
            (Employee.email.ilike(f'%{search}%'))
        )

    query = query.order_by(getattr(Employee, sort))
    employees = query.paginate(page=page, per_page=20)

    return render_template(
        'rgz/employees.html',
        employees=employees,
        student=STUDENT
    )


@rgz.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        data = request.form

        if not all(validate_text(data[x]) for x in ['full_name', 'position', 'gender', 'phone', 'email']):
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


@rgz.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    emp = Employee.query.get_or_404(id)

    if request.method == 'POST':
        data = request.form

        if not all(validate_text(data[x]) for x in ['full_name', 'position', 'gender', 'phone', 'email']):
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


@rgz.route('/delete/<int:id>')
@login_required
def delete_employee(id):
    emp = Employee.query.get_or_404(id)
    db_rgz.session.delete(emp)
    db_rgz.session.commit()
    return redirect(url_for('rgz.employees'))
