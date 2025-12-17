from flask import Blueprint, request, render_template, session, g, abort
import sqlite3
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

# Путь к базе данных
DB_PATH = "/home/Semerka54/SUETA/database.db"


# --- Работа с БД ---
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@lab7.teardown_request
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    db = get_db()
    cursor = db.execute('SELECT * FROM films')
    films = cursor.fetchall()
    return [dict(film) for film in films] # превращаем каждую строку в словарь, чтобы Flask мог вернуть JSON


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    db = get_db()
    film = db.execute(
        'SELECT * FROM films WHERE id = ?',
        (id,)
    ).fetchone() # берёт только одну строку

    if film is None:
        abort(404)

    return dict(film)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    db = get_db()
    cur = db.execute(
        'DELETE FROM films WHERE id = ?',
        (id,)
    )
    db.commit()

    if cur.rowcount == 0:
        abort(404)

    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    db = get_db()
    film = request.get_json() # получает данные из тела запроса (JSON)
    errors = {}

    # Извлекаем данные из JSON и убираем лишние пробелы
    title = film.get('title', '').strip()
    title_ru = film.get('title_ru', '').strip()
    year = film.get('year')
    description = film.get('description', '').strip()

    # Проверяем обязательные поля: русское или оригинальное название
    if title_ru == '':
        errors['title_ru'] = 'Русское название обязательно'

    if title_ru == '' and title == '':
        errors['title'] = 'Оригинальное название обязательно, если русское не указано'

    current_year = 2025
    if not year or int(year) < 1895 or int(year) > current_year:
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    if description == '':
        errors['description'] = 'Описание не должно быть пустым'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        return errors, 400

    # Если нет оригинального названия, но есть русское — используем русское
    if title == '' and title_ru != '':
        title = title_ru

    # Обновляем фильм в базе
    cur = db.execute("""
        UPDATE films
        SET title = ?, title_ru = ?, year = ?, description = ?
        WHERE id = ?
    """, (title, title_ru, year, description, id))

    db.commit()

    if cur.rowcount == 0:
        abort(404)

    return film


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    db = get_db()
    film = request.get_json()
    errors = {}

    title = film.get('title', '').strip()
    title_ru = film.get('title_ru', '').strip()
    year = film.get('year')
    description = film.get('description', '').strip()

    if title_ru == '':
        errors['title_ru'] = 'Русское название обязательно'

    if title_ru == '' and title == '':
        errors['title'] = 'Оригинальное название обязательно, если русское не указано'

    current_year = 2025
    if not year or int(year) < 1895 or int(year) > current_year:
        errors['year'] = f'Год должен быть от 1895 до {current_year}'

    if description == '':
        errors['description'] = 'Описание не должно быть пустым'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'

    if errors:
        return errors, 400

    if title == '' and title_ru != '':
        title = title_ru

    cursor = db.execute("""
        INSERT INTO films (title, title_ru, year, description)
        VALUES (?, ?, ?, ?)
    """, (title, title_ru, year, description))

    db.commit()
    return str(cursor.lastrowid), 201
