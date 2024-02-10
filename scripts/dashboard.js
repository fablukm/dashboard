document.addEventListener('DOMContentLoaded', function() {
    updateWeather(); // Call immediately then set interval
    setInterval(updateWeather, 30000); // Update weather twice per minute

    updateEvents();
    setInterval(updateEvents, 30000); // Update events twice per minute

    updateTransport();
    setInterval(updateTransport, 20000); // Update transport three times per minute

    updateEmails();
    setInterval(updateEmails, 20000); // Update emails twice per minute
});