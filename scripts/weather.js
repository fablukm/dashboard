async function updateWeather() {
    const response = await fetch('/dashboard');
    const data = await response.json();

    document.getElementById('location').textContent = `${data.time_weather.location}`;
    document.getElementById('time').textContent = `${data.time_weather.time}`;
    const weatherIconHtml = chooseWeatherIcon(data.time_weather.weatherId);
    document.getElementById('weather-icon').innerHTML = weatherIconHtml;

    const additionalLocationsContainer = document.getElementById('additional-locations');
    additionalLocationsContainer.innerHTML = ''; // Clear previous entries
    data.time_weather.additional_locations.forEach(location => {
        const weatherIconHtml = chooseWeatherIcon(location.weatherId);
        const div = document.createElement('div');
        div.innerHTML = `<h3>${location.location}</h3><p>${location.time}</p>${weatherIconHtml}`;
        additionalLocationsContainer.appendChild(div);
    });
}

function chooseWeatherIcon(weatherId) {
    // Your existing function here
}