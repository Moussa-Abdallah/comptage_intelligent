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
document.getElementById("stop-btn").addEventListener("click", () => {
    fetch("/stop_detection", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText = data.status;
        })
        .catch(() => {
            document.getElementById("status").innerText = "Erreur backend";
        });
});

let setID= setInterval(() => {
  fetch("/parking_status")
    .then(res => res.json())
    .then(data => {
      document.getElementById("free").innerText = data.free;
      document.getElementById("occupied").innerText = data.occupied;
      document.getElementById("total").innerText = data.total;
    });
}, 500);
