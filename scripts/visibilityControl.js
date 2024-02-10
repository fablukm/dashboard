async function adjustLocationVisibility() {
    // Fetch the location configurations
    const response = await fetch('/configs/locations.json');
    const locations = await response.json();

    locations.forEach((location, index) => {
        // Skip the first location since it's always visible (Main location)
        if (index === 0) return;

        // Calculate the element ID suffix (1 for location1, 2 for location2, etc.)
        const elementIdSuffix = index;
        const locationDiv = document.getElementById(`location${elementIdSuffix}`);
        
        if (locationDiv) {
            // Set the display style based on the "visible" property of the location
            locationDiv.style.display = location.visible ? "" : "none";
        }
    });
}