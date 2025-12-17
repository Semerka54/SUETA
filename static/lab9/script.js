document.addEventListener("DOMContentLoaded", loadState);

function loadState() {
    fetch("/lab9/state", { method: "POST" })
        .then(r => r.json())
        .then(data => {
            document.getElementById("counter").textContent = data.unopened;

            const field = document.getElementById("field");
            field.innerHTML = "";

            data.boxes.forEach(box => {
                const img = document.createElement("img");
                img.src = box.image;
                img.className = "box";
                img.style.left = box.x + "%";
                img.style.top = box.y + "%";

                img.onclick = () => openBox(box.id);

                field.appendChild(img);
            });
        });
}

function openBox(id) {
    fetch("/lab9/open", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id })
    })
    .then(r => {
        if (!r.ok)
            return r.json().then(d => alert(d.error));
        return r.json();
    })
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
