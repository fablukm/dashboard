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
    // OpenWeatherMap weather conditions and corresponding FontAwesome icons
    if (weatherId >= 200 && weatherId <= 232) {
        return '<i class="fas fa-poo-storm"></i>'; // Thunderstorm
    } else if (weatherId >= 300 && weatherId <= 321) {
        return '<i class="fas fa-cloud-rain"></i>'; // Drizzle
    } else if (weatherId >= 500 && weatherId <= 531) {
        return '<i class="fas fa-cloud-showers-heavy"></i>'; // Rain
    } else if (weatherId >= 600 && weatherId <= 622) {
        return '<i class="fas fa-snowflake"></i>'; // Snow
    } else if (weatherId >= 701 && weatherId <= 781) {
        return '<i class="fas fa-smog"></i>'; // Atmosphere
    } else if (weatherId === 800) {
        return '<i class="fas fa-sun"></i>'; // Clear
    } else if (weatherId >= 801 && weatherId <= 804) {
        return '<i class="fas fa-cloud"></i>'; // Clouds
    } else {
        return '<i class="fas fa-question"></i>'; // Unknown
    }
}