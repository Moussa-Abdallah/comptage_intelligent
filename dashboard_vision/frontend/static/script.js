document.getElementById("capture-btn").addEventListener("click", () => {
    fetch("/capture", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText = data.status;
        })
        .catch(() => {
            document.getElementById("status").innerText = "Erreur backend";
        });
});

document.getElementById("generate-btn").addEventListener("click", () => {
    fetch("/generate_json", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText = data.status;
        })
        .catch(() => {
            document.getElementById("status").innerText = "Erreur backend";
        });
});

document.getElementById("run-btn").addEventListener("click", () => {
    fetch("/run_detection", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText = data.status;
        })
        .catch(() => {
            document.getElementById("status").innerText = "Erreur backend";
        });
});