document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("create-event"))
        document.getElementById("create-event").addEventListener("click", createEvent);
    
    if (document.getElementById("edit-event-toggle"))
        document.getElementById("edit-event-toggle").addEventListener("click", toggleEditForm);
    
    if (document.getElementById("delete-event"))
        document.getElementById("delete-event").addEventListener("click", deleteEvent);
    
    if (document.getElementById("recommend-speaker"))
        document.getElementById("recommend-speaker").addEventListener("click", recommendSpeaker);
    
    if (document.getElementById("recommend-space"))
        document.getElementById("recommend-space").addEventListener("click", recommendSpace);
    
    if (document.getElementById("save-event"))
        document.getElementById("save-event").addEventListener("click", saveEditedEvent);
    
    if (document.getElementById("cancel-edit"))
        document.getElementById("cancel-edit").addEventListener("click", hideEditForm);

    if (document.getElementById("event-list"))
        loadEventList();
});

async function createEvent() {
    let name = document.getElementById("event-name").value;
    let eventType = document.getElementById("event-type").value;
    let date = document.getElementById("event-date").value;

    if (!name || !eventType || !date) {
        alert("Debe completar todos los campos");
        return;
    }

    try {
        let response = await fetch("http://localhost:8000/api/events", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, event_type: eventType, date })
        });

        let data = await response.json();
        alert("Evento creado: " + data.name);
    } catch (error) {
        alert("Error al crear evento: " + error.message);
    }
}

function toggleEditForm() {
    let editForm = document.getElementById("edit-form");
    let mainForm = document.getElementById("main-form");

    if (editForm.style.display === "none") {
        editForm.style.display = "block";
        mainForm.style.display = "none";
        loadEventList();  // Recargar la lista de eventos
    } else {
        editForm.style.display = "none";
        mainForm.style.display = "block";
    }
}

// Cargar eventos en la lista desplegable
async function loadEventList() {
    try {
        let response = await fetch("http://localhost:8000/api/events");
        let events = await response.json();

        let eventList = document.getElementById("event-list");
        eventList.innerHTML = "";

        events.forEach(event => {
            let option = document.createElement("option");
            option.value = event.id;
            option.textContent = `${event.name} - ${event.date}`;
            eventList.appendChild(option);
        });

        // Cargar detalles del primer evento automáticamente
        if (events.length > 0) {
            loadEventDetails(events[0].id);
        }

        eventList.addEventListener("change", () => loadEventDetails(eventList.value));
    } catch (error) {
        console.error("Error al cargar eventos:", error);
    }
}

// Cargar detalles del evento seleccionado
async function loadEventDetails(eventId) {
    try {
        let response = await fetch(`http://localhost:8000/api/events/${eventId}`);
        let event = await response.json();

        document.getElementById("edit-event-name").value = event.name;
        document.getElementById("edit-event-type").value = event.event_type;
        document.getElementById("edit-event-date").value = event.date.split(".")[0];  // Formato correcto para input datetime-local
    } catch (error) {
        console.error("Error al cargar detalles del evento:", error);
    }
}

// Guardar cambios en un evento
async function saveEditedEvent() {
    let eventId = document.getElementById("event-list").value;
    let name = document.getElementById("edit-event-name").value;
    let eventType = document.getElementById("edit-event-type").value;
    let date = document.getElementById("edit-event-date").value;

    if (!eventId || !name || !eventType || !date) {
        alert("Todos los campos son obligatorios.");
        return;
    }

    try {
        let response = await fetch(`http://localhost:8000/api/events/${eventId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, event_type: eventType, date })
        });

        let data = await response.json();
        if (response.ok) {
            alert("Evento actualizado correctamente.");
            toggleEditForm();  // Volver al formulario principal
            loadEventList();
        } else {
            console.error("Error al actualizar:", data);
            alert("Error: " + data.detail);
        }
    } catch (error) {
        console.error("Error en la petición:", error);
        alert("Error en la conexión con el servidor.");
    }
}

// Ocultar el formulario de edición y regresar al principal
function hideEditForm() {
    document.getElementById("edit-form").style.display = "none";
    document.getElementById("main-form").style.display = "block";
}

async function deleteEvent() {
    let eventId = prompt("Ingrese el ID del evento a eliminar:");
    let response = await fetch(`http://localhost:8000/api/events/${eventId}`, { method: "DELETE" });
    let data = await response.json();
    alert(data.message);
}

async function generateReport() {
    window.open("http://localhost:8000/api/reports");
}

async function recommendSpeaker() {
    let eventType = document.getElementById("event-type").value;

    if (!eventType) {
        alert("Seleccione un tipo de evento");
        return;
    }

    try {
        let response = await fetch(`http://localhost:8000/api/recommend/speaker/${eventType}`);
        if (!response.ok) throw new Error("No se encontró un speaker para este tipo de evento");

        let data = await response.json();
        let speakerField = document.getElementById("recommended-speaker");

        if (speakerField) {
            speakerField.value = data.speaker;
        } else {
            alert(`Speaker recomendado: ${data.speaker}`);
        }
    } catch (error) {
        alert("Error al obtener la recomendación de speaker: " + error.message);
    }
}


async function recommendSpace() {
    let numAttendees = document.getElementById("num-attendees").value;

    if (!numAttendees || isNaN(numAttendees) || numAttendees <= 0) {
        alert("Ingrese un número válido de asistentes");
        return;
    }

    try {
        let response = await fetch(`http://localhost:8000/api/recommend/space/${numAttendees}`);
        if (!response.ok) throw new Error("No se encontró un espacio adecuado");

        let data = await response.json();
        alert(`Espacio recomendado: ${data.space}`);
    } catch (error) {
        alert("Error al obtener la recomendación de espacio: " + error.message);
    }
}
async function editEvent() {
    let eventId = prompt("Ingrese el ID del evento a editar:");
    let name = prompt("Nuevo nombre del evento:");
    let eventType = prompt("Nuevo tipo de evento:");
    let date = prompt("Nueva fecha y hora (YYYY-MM-DD HH:MM):");

    let response = await fetch(`http://localhost:8000/api/events/${eventId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, event_type: eventType, date })
    });

    let data = await response.json();
    alert(data.message);
}

async function openReportForm() {
    let eventId = prompt("Ingrese el ID del evento que quiere calificar:");
    if (!eventId) return;

    let rating = prompt("Califique el evento (1-5):");
    let organization = prompt("Califique la organización (1-5):");
    let speaker_quality = prompt("Califique la calidad del speaker (1-5):");
    let venue_satisfaction = prompt("Califique el espacio donde se realizó el evento (1-5):");
    let engagement = prompt("¿Cómo califica la interacción con los asistentes? (1-5)");
    let logistics = prompt("¿Cómo califica la logística del evento? (1-5)");
    let feedback = prompt("Ingrese un comentario sobre el evento:");

    if (!rating || !organization || !speaker_quality || !venue_satisfaction || !engagement || !logistics || !feedback) {
        alert("Debe completar todas las preguntas.");
        return;
    }

    try {
        let response = await fetch("http://localhost:8000/api/reports", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                event_id: eventId,
                rating,
                organization,
                speaker_quality,
                venue_satisfaction,
                engagement,
                logistics,
                feedback
            })
        });

        let data = await response.json();
        if (data.id) {
            alert("Reporte generado correctamente. Ahora puedes descargarlo.");
            window.open(`http://localhost:8000/api/reports/download/${eventId}`, "_blank");
        } else {
            alert("Error al generar el reporte.");
        }
    } catch (error) {
        alert("Error al generar reporte: " + error.message);
    }
}

async function generateReport() {
    let eventId = document.getElementById("event-id").value;
    let rating = document.getElementById("rating").value;
    let organization = document.getElementById("organization").value;
    let speaker_quality = document.getElementById("speaker-quality").value;
    let venue_satisfaction = document.getElementById("venue-satisfaction").value;
    let engagement = document.getElementById("engagement").value;
    let logistics = document.getElementById("logistics").value;
    let feedback = document.getElementById("feedback").value;

    if (!eventId || !rating || !organization || !speaker_quality || !venue_satisfaction || !engagement || !logistics || !feedback) {
        alert("Debe completar todas las preguntas.");
        return;
    }

    let response = await fetch("http://localhost:8000/api/reports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            event_id: eventId,
            rating,
            organization,
            speaker_quality,
            venue_satisfaction,
            engagement,
            logistics,
            feedback
        })
    });

    let data = await response.json();
    if (data.id) {
        alert("Reporte generado correctamente. Ahora puedes descargarlo.");
        window.open(`http://localhost:8000/api/reports/download/${eventId}`, "_blank");
    } else {
        alert("Error al generar el reporte.");
    }
}
