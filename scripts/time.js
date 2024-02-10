// This function assumes you can access the locations.json from a public directory
async function fetchLocationsAndUpdateTime() {
    const response = await fetch('configs/locations.json');
    const locations = await response.json();

    // Assuming your locations.json is an array of location objects
    // e.g., [{"name": "City", "timezone": "Europe/Timezone"}, ...]
    locations.forEach(location => {
        const currentTime = getCurrentTimeForTimezone(location.timezone);
        // Update your HTML accordingly. This example assumes you have placeholders
        // for each location's time. You might need to adjust this based on your actual HTML structure.
        const locationElement = document.getElementById(`time-${location.name}`);
        if (locationElement) {
            locationElement.textContent = `${location.name}: ${currentTime}`;
        }
    });
}

function getCurrentTimeForTimezone(timezone) {
    return new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZone: timezone
    }).format(new Date());
}