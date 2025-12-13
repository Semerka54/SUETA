from flask import Blueprint, request, render_template, session, g, abort
import sqlite3

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')


films = [
  {
    "title": "Inception",
    "title_ru": "Начало",
    "year": 2010,
    "description": "Научно-фантастический триллер о воре, который проникает в сны, чтобы украсть или внедрить идею."
  },
  {
    "title": "The Matrix",
    "title_ru": "Матрица",
    "year": 1999,
    "description": "Хакер узнаёт, что реальность — это симуляция, созданная искусственным интеллектом."
  },
  {
    "title": "Interstellar",
    "title_ru": "Интерстеллар",
    "year": 2014,
    "description": "Команда исследователей путешествует через червоточину, чтобы найти новую обитаемую планету."
  },
  {
    "title": "The Shawshank Redemption",
    "title_ru": "Побег из Шоушенка",
    "year": 1994,
    "description": "История несправедливо осуждённого банкира, который не теряет надежды на свободу."
  },
  {
    "title": "The Lord of the Rings: The Fellowship of the Ring",
    "title_ru": "Властелин колец: Братство кольца",
    "year": 2001,
    "description": "Хоббит Фродо отправляется в опасное путешествие, чтобы уничтожить могущественное Кольцо Всевластья."
  }
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    # Проверка корректности id
    if id < 0 or id >= len(films):
        abort(404)
    
    # Удаление фильма
    del films[id]
    
    # Возвращаем успешный ответ без содержимого
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    # Проверка корректности id
    if id < 0 or id >= len(films):
        abort(404)
    # Получение данных из запроса
    film = request.get_json()
    if film['description'] == '':
            return {'description': 'Заполните описание'}, 400
    if film.get('title_ru') and film.get('title') == '':
        film['title'] = film['title_ru']
    # Обновление фильма
    films[id] = film
    # Возврат обновленного фильма
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    # Получение данных о новом фильме из тела запроса
    film = request.get_json()
    if film.get('description', '') == '':
        return {'description': 'Заполните описание'}, 400
    if film.get('title_ru') and film.get('title') == '':
        film['title'] = film['title_ru']
    # Добавление нового фильма в конец списка
    films.append(film)
    # Возвращаем индекс нового элемента (последний индекс в списке)
    # который равен новой длине списка минус 1
    new_index = len(films) - 1
    return str(new_index), 201  