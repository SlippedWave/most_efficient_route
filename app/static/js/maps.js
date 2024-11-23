let map;
let directionsService;
let directionsRenderer;
let currentPositionMarker;
let watchId; // To track the GPS watch process

function initMap() {
    const defaultLocation = { lat: 20.66682, lng: -103.39182 }; 

    map = new google.maps.Map(document.getElementById("map"), {
        center: defaultLocation,
        zoom: 12,
    });

    // Configure the Directions Service and Renderer
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        panel: document.getElementById("directions-panel"),
        suppressMarkers: false,
    });

    // Initial address
    const startAddress = "Blvd. Gral. Marcelino García Barragán 1421, Olímpica, 44430 Guadalajara, Jal";

    // Extract package addresses
    const packageAddresses = uniqueAddresses.map((pkg) => pkg.address);

    // Build the list of addresses for the route (start, packages, end)
    const addresses = [startAddress, ...packageAddresses, startAddress];

    // Geocode the addresses and show the initial route
    geocodeAndDisplayRoute(addresses);

    // Start tracking the driver's location
    trackDriverPosition();
}

async function geocodeAndDisplayRoute(addresses) {
    const geocodedLocations = [];
    const geocoder = new google.maps.Geocoder();

    // Geocode all addresses
    for (const address of addresses) {
        try {
            const location = await geocodeAddress(geocoder, address);
            geocodedLocations.push(location);
        } catch (error) {
            console.error("Geocoding failed:", error.message);
        }
    }

    // Draw the route if geocoding succeeded
    if (geocodedLocations.length === addresses.length) {
        drawRoute(geocodedLocations);
    }
}

function geocodeAddress(geocoder, address) {
    return new Promise((resolve, reject) => {
        geocoder.geocode({ address }, (results, status) => {
            if (status === "OK") {
                resolve(results[0].geometry.location);
            } else {
                reject(new Error(`Geocode failed for ${address}: ${status}`));
            }
        });
    });
}

function drawRoute(locations, currentPosition = null) {
    const waypoints = locations.slice(1, -1).map((location) => ({
        location,
        stopover: true,
    }));

    const request = {
        origin: currentPosition || locations[0], // Use driver's position if available
        destination: locations[locations.length - 1],
        waypoints: waypoints,
        travelMode: "DRIVING",
        optimizeWaypoints: true,
        drivingOptions: {
            departureTime: new Date(),
            trafficModel: "bestguess",
        },
    };

    directionsService.route(request, (result, status) => {
        if (status === "OK") {
            directionsRenderer.setDirections(result);
        } else {
            console.error("Directions request failed:", status);
        }
    });
}

function trackDriverPosition() {
    if (navigator.geolocation) {
        watchId = navigator.geolocation.watchPosition(
            (position) => {
                const currentPosition = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };

                // Update marker for the driver's position
                updateDriverMarker(currentPosition);

                // Update route based on the driver's current location
                const packageAddresses = uniqueAddresses.map((pkg) => pkg.address);
                const addresses = [...packageAddresses, "Blvd. Gral. Marcelino García Barragán 1421, Olímpica, 44430 Guadalajara, Jal"];
                geocodeAndDisplayRoute(addresses.map(addr => currentPosition || addr));
            },
            (error) => {
                console.error("Error getting the current position:", error.message);
            },
            {
                enableHighAccuracy: true, // Use GPS if available for precise tracking
                timeout: 10000, // Maximum wait time for a location update
            }
        );
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

function updateDriverMarker(position) {
    if (!currentPositionMarker) {
        currentPositionMarker = new google.maps.Marker({
            position: position,
            map: map,
            title: "Your Position",
            icon: {
                url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png", // Custom driver icon
            },
        });
    } else {
        currentPositionMarker.setPosition(position);
    }

    // Center the map on the driver's position
    map.setCenter(position);
}

// Stop tracking the driver's position
function stopTracking() {
    if (navigator.geolocation && watchId) {
        navigator.geolocation.clearWatch(watchId);
        watchId = null;
    }
}

// Initialize the map after the page loads
window.onload = initMap;
