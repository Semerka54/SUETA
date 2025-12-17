function fillFilmList() {
    fetch('/lab7/rest-api/films/') // Отправляем HTTP-запрос GET на сервер (Flask REST API), чтобы получить список фильмов
    .then(function(data) {
        return data.json(); // Сервер возвращает JSON → превращаем его в JavaScript-объект (films)
    })
    .then(function (films) {  
        let tbody = document.getElementById('film-list'); // Находим <tbody> таблицы, где будем показывать фильмы
        tbody.innerHTML = ''; // Очищаем таблицу перед заполнением новыми данными
        for(let i = 0; i < films.length; i++) { // Создаём <tr> (строку таблицы) и <td> (ячейки) для каждого фильма
            let tr = document.createElement('tr');
            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            // Устанавливаем значения
            tdTitle.innerText = films[i].title_ru ? films[i].title_ru : films[i].title;

            if (films[i].title_ru && films[i].title) {
                tdTitleRus.innerHTML = `<i>(${films[i].title})</i>`;
            } else {
                tdTitleRus.innerText = '';
            }
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            tdActions.append(editButton);
            tdActions.append(delButton);

            // Добавляем ячейки в строку → строку в таблицу
            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);
            tbody.append(tr);
        }
    })  
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'}) // отправляем DELETE-запрос на сервер для удаления фильма
    .then(function () {
        fillFilmList(); // После удаления вызываем fillFilmList(), чтобы обновить таблицу
    });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block'; // Показываем модальное окно

    // Очищаем старые ошибки перед заполнением формы
    document.getElementById('title-error').innerText = '';
    document.getElementById('title_ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
}


function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

// Скрываем модальное окно, например при отмене
function cancel() {
    hideModal();
}


function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

// Сначала очищаем старые ошибки
function sendFilm() {
    document.getElementById('title-error').innerText = '';
    document.getElementById('title_ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
    // Собираем данные формы в объект film
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    const url = `/lab7/rest-api/films/${id}`;
    // Если id пустой → это новый фильм → POST, иначе PUT (редактируем)
    const method = id === '' ? 'POST' : 'PUT';

    // Отправляем JSON на сервер.

    // Если ответ успешный (resp.ok) → обновляем таблицу и закрываем модальное окно

    // Если сервер вернул ошибки (например, невалидные поля) → показываем их под соответствующими полями
    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if (errors.title)
            document.getElementById('title-error').innerText = errors.title;

        if (errors.title_ru)
            document.getElementById('title_ru-error').innerText = errors.title_ru;

        if (errors.year)
            document.getElementById('year-error').innerText = errors.year;

        if (errors.description)
            document.getElementById('description-error').innerText = errors.description;
    });
}

// GET-запрос на сервер, чтобы получить данные фильма по id
function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function(data) {
        return data.json();
    })
    // Заполняем форму модального окна данными фильма
    .then(function(film) {
        document.getElementById('id').value = id;
        document.getElementById('title').value = film.title;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        showModal();
    });
}