// scripts/weather.js
async function updateWeather() {
  try {
    Logger.info('Fetching weather from API at', new Date().toISOString());
    
    const resp = await fetch('/weather');
    const data = await resp.json();
    if (!data || !data.weather_icon) {
      // console.error('Bad /weather response:', data);
      Logger.error('Bad /weather response:', data);
      return;
    }
    Logger.debug('Raw weather API response:', data);

    // Main title & weather
    document.getElementById('location0-title').textContent = data.location;
    document.getElementById('location0-weather').innerHTML =
      `<img src="https://openweathermap.org/img/wn/${data.weather_icon}.png" alt="">`;
    document.getElementById('location0-temp').textContent = `${data.temp}°`;
    // placeholder for 1h forecast
    document.getElementById('location0-future').textContent = '☀️ in 1h';

    // Side locations (just weather & title & temp)
    data.additional_locations.forEach((loc, idx) => {
      const i = idx + 1;
      document.getElementById(`location${i}-title`).textContent = loc.location;
      document.getElementById(`location${i}-weather`).innerHTML =
        `<img src="https://openweathermap.org/img/wn/${loc.weather_icon}.png" alt="">`;
      document.getElementById(`location${i}-temp`).textContent = `${loc.temp}°`;
    });

  } catch (e) {
    console.error('Failed to fetch weather:', e);
  }
}

// update every 90 s
updateWeather();
setInterval(updateWeather, 90000);
