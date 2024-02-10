// async function fetchDashboardData() {
//     const response = await fetch('/dashboard');
//     const data = await response.json();

//     // Time & Weather
//     document.getElementById('location').textContent = `${data.time_weather.location}`;
//     document.getElementById('time').textContent = `${data.time_weather.time}`;
//     // Use the weatherId to get the appropriate icon
//     const weatherIconHtml = chooseWeatherIcon(data.time_weather.weatherId);
//     document.getElementById('weather-icon').innerHTML = weatherIconHtml;  // Note: Using innerHTML to insert the icon
    

//     // Additional Locations
//     const additionalLocationsContainer = document.getElementById('additional-locations');
//     data.time_weather.additional_locations.forEach(location => {
//         // Assuming each location now includes a `weatherId` you can use to get the icon
//         const weatherIconHtml = chooseWeatherIcon(location.weatherId); // Use the weatherId to get the icon HTML
//         const div = document.createElement('div');
//         div.innerHTML = `<h3>${location.location}</h3><p>${location.time}</p>${weatherIconHtml}`; // Insert the icon HTML directly
//         additionalLocationsContainer.appendChild(div);
//     });

//     // Events
//     const eventsList = document.getElementById('events-list');
//     data.events.forEach(event => {
//         const li = document.createElement('li');
//         li.textContent = `${event.name} - ${event.time}`;
//         eventsList.appendChild(li);
//     });

//     // Unread Emails
//     document.getElementById('unread-emails').textContent = `You have ${data.unread_emails} unread emails.`;

//     // Public Transport
//     const transportList = document.getElementById('transport-list');
//     data.public_transport.forEach(connection => {
//         const li = document.createElement('li');
//         li.textContent = `${connection.station}: ${connection.connection}`;
//         transportList.appendChild(li);
//     });
// }

// function chooseWeatherIcon(weatherId) {
//     // OpenWeatherMap weather conditions and corresponding FontAwesome icons
//     if (weatherId >= 200 && weatherId <= 232) {
//         return '<i class="fas fa-poo-storm"></i>'; // Thunderstorm
//     } else if (weatherId >= 300 && weatherId <= 321) {
//         return '<i class="fas fa-cloud-rain"></i>'; // Drizzle
//     } else if (weatherId >= 500 && weatherId <= 531) {
//         return '<i class="fas fa-cloud-showers-heavy"></i>'; // Rain
//     } else if (weatherId >= 600 && weatherId <= 622) {
//         return '<i class="fas fa-snowflake"></i>'; // Snow
//     } else if (weatherId >= 701 && weatherId <= 781) {
//         return '<i class="fas fa-smog"></i>'; // Atmosphere
//     } else if (weatherId === 800) {
//         return '<i class="fas fa-sun"></i>'; // Clear
//     } else if (weatherId >= 801 && weatherId <= 804) {
//         return '<i class="fas fa-cloud"></i>'; // Clouds
//     } else {
//         return '<i class="fas fa-question"></i>'; // Unknown
//     }
// }

// document.addEventListener('DOMContentLoaded', function() {
//     fetchDashboardData();
// });