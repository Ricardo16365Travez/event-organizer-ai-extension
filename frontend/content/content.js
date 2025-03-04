console.log("Event Organizer AI Extension is running!");

async function fetchEvents() {
    let response = await fetch("http://localhost:8000/api/events");
    let events = await response.json();

    console.log("Eventos obtenidos:", events);
}

fetchEvents();