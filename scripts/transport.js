async function updateTransport() {
    const response = await fetch('/dashboard');
    const data = await response.json();

    const transportList = document.getElementById('transport-list');
    transportList.innerHTML = ''; // Clear previous entries
    data.public_transport.forEach(connection => {
        const li = document.createElement('li');
        li.textContent = `${connection.station}: ${connection.connection}`;
        transportList.appendChild(li);
    });
}
