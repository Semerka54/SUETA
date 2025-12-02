from flask import Blueprint, url_for, request, redirect, Response, render_template, abort, make_response, session, current_app
from functools import wraps
import datetime
import json
import os

lab6 = Blueprint('lab6', __name__)

# Файл для хранения данных офисов
OFFICES_FILE = 'offices_data.json'

def load_offices():
    """Загружает данные об офисах из файла"""
    try:
        if os.path.exists(OFFICES_FILE):
            with open(OFFICES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки файла офисов: {e}")
    
    # Если файла нет или ошибка, создаем начальные данные
    offices = []
    for i in range(1, 11):
        offices.append({"number": i, "tenant": ""})
    return offices

def save_offices(offices):
    """Сохраняет данные об офисах в файл"""
    try:
        with open(OFFICES_FILE, 'w', encoding='utf-8') as f:
            json.dump(offices, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения файла офисов: {e}")
        return False

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id', 1)
    method = data.get('method', '')
    
    # Загружаем текущее состояние офисов
    offices = load_offices()
    
    # Метод info доступен всем
    if method == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    # Для остальных методов нужна авторизация
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    # Метод booking
    if method == 'booking':
        office_number = data.get('params')
        office_found = False
        
        for office in offices:
            if office['number'] == office_number:
                office_found = True
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                
                office['tenant'] = login
                save_offices(offices)  # Сохраняем изменения
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
        
        if not office_found:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Office not found'
                },
                'id': id
            }
    
    # Метод cancellation
    if method == 'cancellation':
        office_number = data.get('params')
        office_found = False
        
        for office in offices:
            if office['number'] == office_number:
                office_found = True
                # Проверка арендованности
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                
                # Проверка, что офис арендован текущим пользователем
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'You are not the tenant of this office'
                        },
                        'id': id
                    }
                
                # Снятие аренды
                office['tenant'] = ''
                save_offices(offices)  # Сохраняем изменения
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
        
        if not office_found:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'Office not found'
                },
                'id': id
            }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }