from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session
import datetime
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')