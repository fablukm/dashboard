async function updateEvents() {
    const response = await fetch('/dashboard');
    const data = await response.json();

    const eventsList = document.getElementById('events-list');
    eventsList.innerHTML = ''; // Clear previous entries
    data.events.forEach(event => {
        const li = document.createElement('li');
        li.textContent = `${event.name} - ${event.time}`;
        eventsList.appendChild(li);
    });
}