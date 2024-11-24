let map;
let directionsService;
let directionsRenderer;

function initMap() {
    const defaultLocation = { lat: 20.66682, lng: -103.39182 };

    map = new google.maps.Map(document.getElementById("map"), {
        center: defaultLocation,
        zoom: 12,
        styles: [
            {
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#ebe3cd"
                    }
                ]
            },
            {
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#523735"
                    }
                ]
            },
            {
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#f5f1e6"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#c9b2a6"
                    }
                ]
            },
            {
                "featureType": "administrative.land_parcel",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#dcd2be"
                    }
                ]
            },
            {
                "featureType": "administrative.land_parcel",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#ae9e90"
                    }
                ]
            },
            {
                "featureType": "administrative.province",
                "stylers": [
                    {
                        "color": "#ffeb3b"
                    },
                    {
                        "saturation": -5
                    },
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "landscape.natural",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "poi",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#93817c"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#a5b076"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#447530"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#f5f1e6"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#fdfcf8"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#f8c967"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#e9bc62"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#e98d58"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#db8555"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#806b63"
                    }
                ]
            },
            {
                "featureType": "transit",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#8f7d77"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#ebe3cd"
                    }
                ]
            },
            {
                "featureType": "transit.station",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#b9d3c2"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#92998d"
                    }
                ]
            }
        ],
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true,
    });

    const startAddress = {
        address: "Blvd. Gral. Marcelino García Barragán 1421, Olímpica, 44430 Guadalajara, Jal",
        package: [],
        address_id: 0,
        location: null
    };

    const packageAddresses = uniqueAddresses
        .map(pkg => {
            return {
                address: pkg.address, // Ensure the address is retained
                packages: pkg.packages, // Retain the packages array associated with the address
                address_id: pkg.address_id,
                location: null
            };
        })
        .filter(pkg => pkg.address && typeof pkg.address === "string");

    if (packageAddresses.length === 0) {
        console.error("No valid addresses found.");
        return;
    }

    const addresses = [startAddress, ...packageAddresses, startAddress];
    geocodeAndDisplayRoute(addresses);

    // Add traffic layer
    const trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);
}

// Geocode addresses and display the route
async function geocodeAndDisplayRoute(addresses) {
    const geocoder = new google.maps.Geocoder();

    for (let i = 0; i < addresses.length; i++) {
        try {
            const location = await geocodeAddress(geocoder, addresses[i].address);
            addresses[i].location = location;
        } catch (error) {
            console.error("Geocoding falló para la dirección ", [i].address, error);
        }
    }

    if (addresses.length === addresses.length) {
        drawRoute(addresses);
    } else {
        console.error("Algunas direcciones no pudieron ser codificadas.");
    }
}

// Geocode a single address
function geocodeAddress(geocoder, address) {
    return new Promise((resolve, reject) => {
        geocoder.geocode({ address }, (results, status) => {
            if (status === "OK") {
                resolve(results[0].geometry.location);
            } else {
                reject(new Error(`Geocode falló en ${address}: ${status}`));
            }
        });
    });
}
function drawRoute(addresses) {
    // Create waypoints from all addresses except the start and end
    const waypoints = addresses.slice(1, addresses.length - 1).map(locationData => ({
        location: locationData.location,
        stopover: true
    }));

    const request = {
        origin: addresses[0].location,
        destination: addresses[addresses.length - 1].location,
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

            const optimizedOrder = result.routes[0].waypoint_order;

            const optimizedLocations = [
                addresses[0],
                ...optimizedOrder.map(index => addresses[index + 1]),
                addresses[addresses.length - 1],
            ];

            const optimizedAddressMap = optimizedLocations.reduce((map, locationData) => {
                const location = locationData.location;
                const key = `${location.lat()},${location.lng()}`;
                if (!map[key]) {
                    map[key] = locationData;
                }
                return map;
            }, {});

            addCustomMarkers(optimizedAddressMap);
            const googleMapsUrl = generateGoogleMapsUrl(optimizedLocations);
            displayGoogleMapsLink(googleMapsUrl);

            directionsRenderer.setDirections(result);
        } else {
            console.error("Falló request de direcciones:", status);
        }
    });
}

function generateGoogleMapsUrl(locations) {
    const origin = encodeURIComponent(locations[0].location.toString());
    const destination = encodeURIComponent(locations[locations.length - 1].location.toString());
    const waypoints = locations.slice(1, -1)
        .map(location => encodeURIComponent(location.location.toString()))
        .join("|");

    return `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}&waypoints=${waypoints}`;
}

function displayGoogleMapsLink(url) {
    const linkContainer = document.getElementById("google-maps-link-container");
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.textContent = "Abrir esta ruta en Google Maps";
    linkContainer.innerHTML = '';
    linkContainer.appendChild(link);
}

function addCustomMarkers(optimizedAddressMap) {
    Object.keys(optimizedAddressMap).forEach((address, index) => {
        const locationData = optimizedAddressMap[address];
        const location = locationData.location;
        const add = locationData.address;
        const address_id = locationData.address_id;

        const marker = new google.maps.Marker({
            position: location,
            map: map,
            title: `Location ${index + 1}`,
            icon: index === 0
                ? "https://maps.google.com/mapfiles/ms/icons/green-dot.png"
                : "https://maps.google.com/mapfiles/ms/icons/red-dot.png"
        });

        const infoWindowContent = index !== 0
            ?
            ` 
            <div>
                <p><strong>Ubicación:</strong> ${add}</p>
                <button class="btn btn-primary" onclick="openPackageModal(${address_id})">View Packages</button>
            </div>
            `
            :
            `
            <div>
                <p><strong>Ubicación:</strong> ${add}</p>
                <p><strong>Esta es la matriz</strong></p>
            </div>
            `;

        const infoWindow = new google.maps.InfoWindow({
            content: infoWindowContent,
        });

        // Add click listener to marker
        marker.addListener("click", () => {
            infoWindow.open(map, marker);
        });
    });
}

// Open the package details modal
function openPackageModal(address_id) {
    const tableBody = document.querySelector("#package-details-table tbody");

    const packageData = uniqueAddresses.find(address => address.address_id === address_id)?.packages;

    tableBody.innerHTML = '';

    if (packageData && packageData.length > 0) {
        packageData.forEach(pkg => {
            const row = document.createElement("tr");
            row.id = pkg.PCK_packageId;
            row.innerHTML = `
                <td>${pkg.PCK_packageId || 'N/A'}</td>
                <td>${pkg.PCK_client_name || 'N/A'}</td>
                <td>${pkg.PCK_client_phone_num || 'N/A'}</td>
                <td>${pkg.status || 'N/A'}</td>
                <td>${pkg.PCK_delivery_date || 'N/A'}</td>
                <td>${pkg.PCK_special_delivery_instructions || 'None'}</td>
                <td>
                    <button class="btn btn-warning"
                        onclick="openSetStatusModal('${pkg.PCK_packageId}')"
                        data-id="${pkg.PCK_packageId}">
                        Modificar
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } else {
        const emptyRow = document.createElement("tr");
        emptyRow.innerHTML = `
            <td colspan="5" class="text-center">No hay paquetes disponibles.</td>
        `;
        tableBody.appendChild(emptyRow);
    }

    const modal = new bootstrap.Modal(document.getElementById("package-modal"), {
        backdrop: 'static',
        keyboard: true,
    });
    modal.show();
}

function openSetStatusModal(PCK_packageId) {
    let input_packageId = document.getElementById("value_packageId").value = PCK_packageId;
    const modal = new bootstrap.Modal(document.getElementById("package-set-status-modal"), {
        backdrop: 'static',
        keyboard: true,
    })
    modal.show();
};

function setNewStatusPackage() {
    let PCK_packageId = document.getElementById("value_packageId").value;
    let new_package_status = document.getElementById("value_new_package_status").value;

    if (!PCK_packageId || !new_package_status) {
        console.log("ERROR, NO ESTAN LOS DATOS")
        return;
    }

    $.ajax({
        url: '/ver_mi_ruta_de_entrega',
        type: 'POST',
        data: {
            packageId: PCK_packageId,
            status: new_package_status
        },
        success: function () {
            updateStatusInTable(PCK_packageId, new_package_status, '#package-details-table');
            updateStatusInTable(PCK_packageId, new_package_status, '#management_table');
            const modal = bootstrap.Modal.getInstance(document.getElementById("package-set-status-modal"));
            modal.hide();

        },
        error: function (xhr, status, error) {
            bootbox.alert("Failed to update package status. Please try again.");
        }
    });
}

function updateStatusInTable(packageId, newStatus, table) {
    const tableRow = document.querySelector(`${table} tbody tr[id="${packageId}"]`);

    if (tableRow) {
        const statusCell = tableRow.querySelector('td:nth-child(4)');

        if (statusCell) {
            statusCell.textContent = newStatus == 3 ? "ENTREGADO" : "POR ENTREGAR";
        } else {
            console.warn(`Status cell not found for package ID ${packageId}.`);
        }
    } else {
        console.warn(`Row for package ID ${packageId} not found.`);
    }
}




window.onload = initMap;
