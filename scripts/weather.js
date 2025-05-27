// scripts/weather.js
async function updateWeather() {
  const resp = await fetch('/weather');
  const data = await resp.json();
  if (!data || !data.weather_icon) {
    console.error('Bad /weather response:', data);
    return;
  }

  // Current time
  const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // Main sector
  document.getElementById('location0-time').textContent = now;
  document.getElementById('location0-title').textContent = data.location;
  document.getElementById('location0-weather').innerHTML =
    `<img src="https://openweathermap.org/img/wn/${data.weather_icon}.png" alt="">`;
  document.getElementById('location0-temp').textContent = `${data.temp}°`;
  // placeholder for future forecast
  document.getElementById('location0-future').textContent = '☀️ in 1h';

  // Side sectors
  data.additional_locations.forEach((loc, idx) => {
    const i = idx + 1;
    document.getElementById(`location${i}-title`).textContent = loc.location;
    document.getElementById(`location${i}-time`).textContent = now;
    document.getElementById(`location${i}-weather`).innerHTML =
      `<img src="https://openweathermap.org/img/wn/${loc.weather_icon}.png" alt="">`;
    document.getElementById(`location${i}-temp`).textContent = `${loc.temp}°`;
  });
}

// Kick off & refresh every minute
updateWeather();
setInterval(updateWeather, 60000);
