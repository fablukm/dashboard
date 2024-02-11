async function updateTime() {
    // Fetch the location configurations
    const response = await fetch('/configs/locations.json');
    const locations = await response.json();

    // Update location time
    updateLocationTime(locations[0], 'location0');
    updateLocationTime(locations[1], 'location1');
    updateLocationTime(locations[2], 'location2');
}

function updateMainLocationTime(location) {
    const currentTime = getCurrentTimeForTimezone(location.timezone);
    document.getElementById('location0-title').textContent = location.displayname;
    document.getElementById('location0-time').textContent = currentTime;
}

function updateLocationTime(location, elementIdPrefix) {
    const currentTime = getCurrentTimeForTimezone(location.timezone);
    document.getElementById(`${elementIdPrefix}-title`).textContent = location.displayname;
    document.getElementById(`${elementIdPrefix}-time`).textContent = currentTime;
}

function getCurrentTimeForTimezone(timezone) {
    return new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: timezone,
        hour12: false // Use 24-hour time format
    }).format(new Date());
}