from flask import Blueprint, render_template, request, jsonify, session, redirect
import random

lab9 = Blueprint('lab9', __name__)

BOX_COUNT = 10
boxes = []

congratulations = [
    "С Новым годом!",
    "Счастья и здоровья!",
    "Пусть сбудутся мечты!",
    "Удачи в новом году!",
    "Тепла и уюта!",
    "Радости каждый день!",
    "Новых побед!",
    "Хорошего настроения!",
    "Исполнения желаний!",
    "Успехов во всём!"
]

MIN_DISTANCE = 15  # минимальное расстояние между коробками (в процентах)

# --------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# --------------------------------------------------

def is_far_enough(x, y, existing):
    for box in existing:
        dx = x - box["x"]
        dy = y - box["y"]
        if (dx * dx + dy * dy) ** 0.5 < MIN_DISTANCE:
            return False
    return True


def init_boxes():
    if boxes:
        return

    random.shuffle(congratulations)

    for i in range(BOX_COUNT):
        while True:
            x = random.randint(10, 90)
            y = random.randint(10, 80)

            if is_far_enough(x, y, boxes):
                boxes.append({
                    "id": i,
                    "x": x,
                    "y": y,
                    "opened": False,
                    "text": congratulations[i],
                    "image": f"/static/lab9/box{i}.png",
                    "auth_only": i % 3 == 0  # некоторые подарки только для авторизованных
                })
                break


# --------------------------------------------------
# ОСНОВНАЯ СТРАНИЦА
# --------------------------------------------------

@lab9.route('/lab9/')
def page():
    init_boxes()
    session.setdefault("opened_count", 0)
    session.setdefault("auth", False)
    return render_template("lab9/index.html")


# --------------------------------------------------
# АВТОРИЗАЦИЯ (упрощённая)
# --------------------------------------------------

@lab9.route('/lab9/login')
def login():
    session["auth"] = True
    return redirect('/lab9/')


@lab9.route('/lab9/logout')
def logout():
    session["auth"] = False
    session["opened_count"] = 0
    return redirect('/lab9/')


# --------------------------------------------------
# API
# --------------------------------------------------

@lab9.route('/lab9/state', methods=['POST'])
def state():
    unopened = sum(not b["opened"] for b in boxes)
    return jsonify({
        "boxes": boxes,
        "unopened": unopened,
        "opened_count": session["opened_count"],
        "auth": session["auth"]
    })


@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    box_id = request.json.get("id")
    box = boxes[box_id]

    # ограничение по количеству коробок
    if session["opened_count"] >= 3:
        return jsonify({"error": "Можно открыть не более 3 коробок"}), 403

    # ограничение для неавторизованных
    if box["auth_only"] and not session["auth"]:
        return jsonify({"error": "Этот подарок доступен только авторизованным пользователям"}), 403

    # если коробка уже открыта — ничего не делаем
    if box["opened"]:
        return jsonify({}), 200

    box["opened"] = True
    session["opened_count"] += 1

    return jsonify({
        "text": box["text"],
        "image": box["image"]
    })


@lab9.route('/lab9/reset', methods=['POST'])
def reset_boxes():
    if not session["auth"]:
        return jsonify({"error": "Требуется авторизация"}), 403

    for box in boxes:
        box["opened"] = False

    session["opened_count"] = 0

    return jsonify({"status": "ok"})
