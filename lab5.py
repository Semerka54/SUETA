from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session
from functools import wraps
import datetime
lab5 = Blueprint('lab5', __name__)

@lab5.route("/lab5/")
def lab():
    return render_template("lab5/lab5.html", username="Anonymous")


@lab5.route('/lab5/login')
def login():
    return "Страница входа"


@lab5.route('/lab5/register')
def register():
    return "Страница регистрации"


@lab5.route('/lab5/list')
def articles_list():
    return "Список статей"


@lab5.route('/lab5/create')
def create_article():
    return "Создать статью"