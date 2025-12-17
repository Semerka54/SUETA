from flask import Blueprint, render_template, request, jsonify, session
import random

lab9 = Blueprint('lab9', __name__)

BOX_COUNT = 10
BOX_SIZE = 140
FIELD_WIDTH = 1200
FIELD_HEIGHT = 500
PADDING = 20

boxes = []

USERS = {
    "admin": "1234",
    "user": "qwerty"
}

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


def intersects(x, y, other):
    return not (
        x + BOX_SIZE + PADDING < other["x"] or
        x > other["x"] + BOX_SIZE + PADDING or
        y + BOX_SIZE + PADDING < other["y"] or
        y > other["y"] + BOX_SIZE + PADDING
    )


def init_boxes():
    if boxes:
        return

    random.shuffle(congratulations)

    for i in range(BOX_COUNT):
        for _ in range(1000):
            x = random.randint(0, FIELD_WIDTH - BOX_SIZE)
            y = random.randint(0, FIELD_HEIGHT - BOX_SIZE)

            if all(not intersects(x, y, b) for b in boxes):
                boxes.append({
                    "id": i,
                    "x": x,
                    "y": y,
                    "opened": False,
                    "text": congratulations[i],
                    "image": f"/static/lab9/box{i}.png",
                    "auth_only": i % 3 == 0
                })
                break
        else:
            raise RuntimeError("Не удалось разместить коробки без пересечений")


@lab9.route('/lab9/')
def lab():
    init_boxes()
    session.setdefault("opened_count", 0)
    session.setdefault("user", None)
    return render_template("lab9/index.html")


@lab9.route('/lab9/login', methods=["POST"])
def login():
    data = request.json
    if data["login"] in USERS and USERS[data["login"]] == data["password"]:
        session["user"] = data["login"]
        session["opened_count"] = 0
        return jsonify({"ok": True})
    return jsonify({"error": "Неверный логин или пароль"}), 401


@lab9.route('/lab9/logout', methods=["POST"])
def logout():
    session["user"] = None
    session["opened_count"] = 0
    return jsonify({"ok": True})


@lab9.route('/lab9/state', methods=["POST"])
def state():
    return jsonify({
        "boxes": boxes,
        "unopened": sum(not b["opened"] for b in boxes),
        "opened_count": session["opened_count"],
        "auth": session["user"] is not None,
        "user": session["user"]
    })


@lab9.route('/lab9/open', methods=["POST"])
def open_box():
    box = boxes[request.json["id"]]

    if session["opened_count"] >= 3:
        return jsonify({"error": "Можно открыть не более 3 коробок"}), 403

    if box["auth_only"] and not session["user"]:
        return jsonify({"error": "Требуется авторизация"}), 403

    if box["opened"]:
        return jsonify({})

    box["opened"] = True
    session["opened_count"] += 1

    return jsonify({
        "text": box["text"],
        "image": box["image"]
    })


@lab9.route('/lab9/reset', methods=["POST"])
def reset_boxes():
    if not session["user"]:
        return jsonify({"error": "Требуется авторизация"}), 403

    for box in boxes:
        box["opened"] = False

    session["opened_count"] = 0
    return jsonify({"ok": True})
