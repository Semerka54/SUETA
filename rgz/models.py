from .db_rgz import db_rgz
from werkzeug.security import generate_password_hash, check_password_hash

class Employee(db_rgz.Model):
    __tablename__ = 'employee'
    id = db_rgz.Column(db_rgz.Integer, primary_key=True)
    full_name = db_rgz.Column(db_rgz.String(100), nullable=False)
    position = db_rgz.Column(db_rgz.String(50), nullable=False)
    gender = db_rgz.Column(db_rgz.String(1), nullable=False)
    phone = db_rgz.Column(db_rgz.String(20), nullable=False)
    email = db_rgz.Column(db_rgz.String(100), nullable=False)
    probation = db_rgz.Column(db_rgz.Boolean, default=False)
    hire_date = db_rgz.Column(db_rgz.Date, nullable=False)

class Admin(db_rgz.Model):
    __tablename__ = 'admin'
    id = db_rgz.Column(db_rgz.Integer, primary_key=True)
    username = db_rgz.Column(db_rgz.String(50), unique=True, nullable=False)
    password_hash = db_rgz.Column(db_rgz.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
