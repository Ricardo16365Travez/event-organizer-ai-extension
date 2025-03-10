document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("dark-mode-toggle").addEventListener("click", toggleDarkMode);

    document.getElementById("create-event").addEventListener("click", createEvent);
    document.getElementById("edit-event").addEventListener("click", editEvent);
    document.getElementById("delete-event").addEventListener("click", deleteEvent);
    document.getElementById("generate-report").addEventListener("click", openReportForm);
    document.getElementById("recommend-speaker").addEventListener("click", recommendSpeaker);
    document.getElementById("recommend-space").addEventListener("click", recommendSpace);

    // Aplicar modo oscuro si estaba activado previamente
    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
    }
});

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
}
