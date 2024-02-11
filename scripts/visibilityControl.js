async function adjustLocationVisibility() {
    // Fetch the location configurations
    const response = await fetch('/configs/locations.json');
    const locations = await response.json();

    // Assuming the class name to identify location elements is "location-class"
    // and each location in your JSON has a unique identifier or name that matches part of the class name.
    locations.forEach((location, index) => {
        // Skip the first location since it's always visible (Main location)
        if (index === 0) return;

        // Find all elements with a class name that includes the location's identifier or name
        // Adjust the class name pattern as necessary to match your HTML structure
        const locationElements = document.querySelectorAll(`div.location${index}`);

        locationElements.forEach((element) => {
            // Set the display style based on the "visible" property of the location
            element.style.display = location.visible ? "" : "none";
        });
    });

    // locations.forEach((location, index) => {
    //     // Skip the first location since it's always visible (Main location)
    //     if (index === 0) return;

    //     // Calculate the element ID suffix (1 for location1, 2 for location2, etc.)
    //     const elementIdSuffix = index;
    //     const locationDiv = document.getElementById(`location${elementIdSuffix}`);
        
    //     if (locationDiv) {
    //         // Set the display style based on the "visible" property of the location
    //         locationDiv.style.display = location.visible ? "" : "none";
    //     }
    // });
}