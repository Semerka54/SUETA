from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session
from functools import wraps
import datetime

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def lab():
    return render_template('lab9/index.html')