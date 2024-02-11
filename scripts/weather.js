async function updateWeather() {
    const response = await fetch('/dashboard');
    const data = await response.json();

    // Update main location weather
    // document.getElementById('location0-title').textContent = `${data.weather.location}`;
    document.getElementById('location0-weather').innerHTML = `<img src="http://openweathermap.org/img/wn/${data.weather.weather_icon}.png" alt="Weather Icon">`;
    document.getElementById('location0-temp').innerHTML = `${data.weather.temp}&deg;`;

    data.weather.additional_locations.forEach((location, index) => {
        const locationId = `location${index + 1}`;
        // document.getElementById(`${locationId}-title`).textContent = `${location.location}`;
        document.getElementById(`${locationId}-temp`).innerHTML = `${location.temp}&deg;`;
        document.getElementById(`${locationId}-weather`).innerHTML = `<img src="http://openweathermap.org/img/wn/${location.weather_icon}.png" alt="Weather Icon">`;
    });
}