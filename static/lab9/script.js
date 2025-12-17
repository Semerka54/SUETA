document.addEventListener("DOMContentLoaded", loadState);

function loadState() {
    fetch("/lab9/state", { method: "POST" })
        .then(r => r.json())
        .then(data => {
            document.getElementById("counter").textContent = data.unopened;
            renderAuth(data);
            renderBoxes(data.boxes);
        });
}

function renderAuth(data) {
    const block = document.getElementById("auth-block");

    if (!data.auth) {
        block.innerHTML = `
            <div class="login-form">
                <input id="login" placeholder="Логин">
                <input id="password" type="password" placeholder="Пароль">
                <button onclick="login()">Войти</button>
            </div>`;
        document.getElementById("santa-panel").classList.add("hidden");
    } else {
        block.innerHTML = `
            <div class="user-panel">
                👤 ${data.user}
                <button onclick="logout()">Выйти</button>
            </div>`;
        document.getElementById("santa-panel").classList.remove("hidden");
    }
}

function renderBoxes(boxes) {
    const field = document.getElementById("field");
    field.innerHTML = "";

    boxes.forEach(box => {
        const img = document.createElement("img");
        img.src = box.image;
        img.className = "box";
        img.style.left = box.x + "px";
        img.style.top = box.y + "px";

        if (!box.opened) {
            img.onclick = () => openBox(box.id);
        }

        field.appendChild(img);
    });
}

function login() {
    fetch("/lab9/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            login: document.getElementById("login").value,
            password: document.getElementById("password").value
        })
    })
    .then(r => r.ok ? loadState() : r.json().then(d => alert(d.error)));
}

function logout() {
    fetch("/lab9/logout", { method: "POST" })
        .then(() => loadState());
}

function openBox(id) {
    fetch("/lab9/open", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    })
    .then(r => r.ok ? r.json() : r.json().then(d => alert(d.error)))
    .then(data => {
        if (!data || !data.text) return;
        document.getElementById("message").textContent = data.text;
        document.getElementById("popup-image").src = data.image;
        document.getElementById("popup").classList.remove("hidden");
        loadState();
    });
}

function closePopup() {
    document.getElementById("popup").classList.add("hidden");
}

function resetBoxes() {
    fetch("/lab9/reset", { method: "POST" })
        .then(r => r.ok ? loadState() : r.json().then(d => alert(d.error)));
}
