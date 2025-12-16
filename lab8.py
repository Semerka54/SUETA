from flask import Blueprint, request, render_template, session, g, abort
import sqlite3
from datetime import datetime

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', username='anonymous')

@lab8.route('/lab8/login')
def login():
    return render_template('lab8/login.html')

@lab8.route('/lab8/register')
def register():
    return render_template('lab8/register.html')

@lab8.route('/lab8/articles')
def articles():
    return render_template('lab8/articles.html')

@lab8.route('/lab8/create')
def create():
    return render_template('lab8/create.html')