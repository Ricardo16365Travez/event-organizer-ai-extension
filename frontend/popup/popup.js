document.addEventListener("DOMContentLoaded", async () => {
    loadEvents(); 

    // Manejar el envío del formulario
    document.getElementById("event-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        
        let name = document.getElementById("event-name").value;
        let description = document.getElementById("event-description").value;
        let date = document.getElementById("event-date").value;

        let response = await fetch("http://localhost:8000/api/events", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, description, date, organizer_id: 1 }) 
        });

        if (response.ok) {
            alert("Evento creado con éxito!");
            loadEvents(); 
        } else {
            alert("Error al crear evento");
        }
    });
});

async function loadEvents() {
    try {
        let response = await fetch("http://localhost:8000/api/events");
        let events = await response.json();
        
        let eventsList = document.getElementById("events-list");
        eventsList.innerHTML = "";

        if (!Array.isArray(events)) {
            eventsList.textContent = "No hay eventos disponibles.";
            return;
        }

        events.forEach(event => {
            let li = document.createElement("li");
            li.innerHTML = `<strong>${event.name}</strong> - ${event.date}
                            <button onclick="deleteEvent(${event.id})">❌</button>`;
            eventsList.appendChild(li);
        });

    } catch (error) {
        console.error("Error al cargar eventos:", error);
    }
}

// Función para eliminar un evento
async function deleteEvent(eventId) {
    let response = await fetch(`http://localhost:8000/api/events/${eventId}`, {
        method: "DELETE"
    });

    if (response.ok) {
        alert("Evento eliminado");
        loadEvents();
    } else {
        alert("Error al eliminar el evento");
    }
}
