from flask import Blueprint, request, render_template, session, g
import sqlite3

lab6 = Blueprint('lab6', __name__)

# Путь к базе данных
DB_PATH = "/home/Semerka54/SUETA/database.db"


# --- Работа с БД ---
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@lab6.teardown_request
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# --- Маршрут страницы ---
@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


# --- JSON-RPC API ---
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    method = data.get("method")
    req_id = data.get("id")
    db = get_db()

    # ----------- METHOD: info -----------
    if method == "info":
        offices = db.execute("SELECT * FROM offices").fetchall()

        return {
            "jsonrpc": "2.0",
            "result": {
                "offices": [dict(o) for o in offices],
                "login": session.get("login")
            },
            "id": req_id
        }

    # ----------- Проверка авторизации -----------
    login = session.get("login")
    if not login:
        return {
            "jsonrpc": "2.0",
            "error": {"code": 1, "message": "Unauthorized"},
            "id": req_id
        }

    # ----------- METHOD: booking -----------
    if method == "booking":
        office_number = data["params"]

        office = db.execute(
            "SELECT tenant FROM offices WHERE number = ?",
            (office_number,)
        ).fetchone()

        if office is None:
            return {"jsonrpc": "2.0",
                    "error": {"code": -32601, "message": "Office not found"},
                    "id": req_id}

        if office["tenant"] != "":
            return {"jsonrpc": "2.0",
                    "error": {"code": 2, "message": "Already booked"},
                    "id": req_id}

        db.execute(
            "UPDATE offices SET tenant = ? WHERE number = ?",
            (login, office_number)
        )
        db.commit()

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}

    # ----------- METHOD: cancellation -----------
    if method == "cancellation":
        office_number = data["params"]

        office = db.execute(
            "SELECT tenant FROM offices WHERE number = ?",
            (office_number,)
        ).fetchone()

        if office is None:
            return {"jsonrpc": "2.0",
                    "error": {"code": -32601, "message": "Office not found"},
                    "id": req_id}

        if office["tenant"] == "":
            return {"jsonrpc": "2.0",
                    "error": {"code": 3, "message": "Office not booked"},
                    "id": req_id}

        if office["tenant"] != login:
            return {"jsonrpc": "2.0",
                    "error": {"code": 4, "message": "Not your booking"},
                    "id": req_id}

        db.execute(
            "UPDATE offices SET tenant = '' WHERE number = ?",
            (office_number,)
        )
        db.commit()

        return {"jsonrpc": "2.0", "result": "success", "id": req_id}

    # ----------- UNKNOWN METHOD -----------
    return {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Method not found"},
        "id": req_id
    }
