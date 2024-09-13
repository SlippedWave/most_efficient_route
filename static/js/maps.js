'use strict';

/**
 * Element selectors for commutes widget.
 */
const commutesEl = {
  map: document.querySelector('.map-view'),
  initialStatePanel: document.querySelector('.commutes-initial-state'),
  destinationPanel: document.querySelector('.commutes-destinations'),
  modal: document.querySelector('.commutes-modal-container'),
};

/**
 * Element selectors for commutes destination panel.
 */
const destinationPanelEl = {
  addButton: commutesEl.destinationPanel.querySelector('.add-button'),
  container: commutesEl.destinationPanel.querySelector('.destinations-container'),
  list: commutesEl.destinationPanel.querySelector('.destination-list'),
  scrollLeftButton: commutesEl.destinationPanel.querySelector('.left-control'),
  scrollRightButton: commutesEl.destinationPanel.querySelector('.right-control'),
  getActiveDestination: () => commutesEl.destinationPanel.querySelector('.destination.active'),
};

/**
 * Element selectors for commutes modal popup.
 */
const destinationModalEl = {
  title: commutesEl.modal.querySelector('h2'),
  form: commutesEl.modal.querySelector('form'),
  destinationInput: commutesEl.modal.querySelector('input[name="destination-address"]'),
  errorMessage: commutesEl.modal.querySelector('.error-message'),
  addButton: commutesEl.modal.querySelector('.add-destination-button'),
  deleteButton: commutesEl.modal.querySelector('.delete-destination-button'),
  editButton: commutesEl.modal.querySelector('.edit-destination-button'),
  cancelButton: commutesEl.modal.querySelector('.cancel-button'),
  getTravelModeInput: () => commutesEl.modal.querySelector('input[name="travel-mode"]:checked'),
};

/**
 * Max number of destination allowed to be added to commutes panel.
 */
const MAX_NUM_DESTINATIONS = 10;

/**
 * Bounds to bias search within ~50km distance.
 */
const BIAS_BOUND_DISTANCE = 0.5;

/**
 * Hour in seconds.
 */
const HOUR_IN_SECONDS = 3600;

/**
 * Minutes in seconds.
 */
const MIN_IN_SECONDS = 60;

/**
 * Stroke colors for destination direction polylines for different states.
 */
const STROKE_COLORS = {
  active: {
    innerStroke: '#4285F4',
    outerStroke: '#185ABC',
  },
  inactive: {
    innerStroke: '#BDC1C6',
    outerStroke: '#80868B',
  },
};

/**
 * Marker icon colors for different states.
 */
const MARKER_ICON_COLORS = {
  active: {
    fill: '#EA4335',
    stroke: '#C5221F',
    label: '#FFF',
  },
  inactive: {
    fill: '#F1F3F4',
    stroke: '#9AA0A6',
    label: '#3C4043',
  },
};

/**
 * List of operations to perform on destinations.
 */
const DestinationOperation = {
  ADD: 'ADD',
  EDIT: 'EDIT',
  DELETE: 'DELETE',
};

/**
 * List of available commutes travel mode.
 */
const TravelMode = {
  DRIVING: 'DRIVING',
};

/**
   * toggles the activation of the generate route button
   */
function setStateGenerateRouteButton(condition) {
  const button = document.getElementById('generate-route-btn'); 
  button.disabled = condition;
}

/**
 * Defines instance of Commutes widget to be instantiated when Map library
 * loads.
 */
function Commutes(configuration) {
  let commutesMap;
  let activeDestinationIndex;
  let origin = configuration.mapOptions.center;
  let destinations = configuration.destination || [];
  let markerIndex = 0;
  let lastActiveEl;

  const markerIconConfig = {
    path:
      'M10 27c-.2 0-.2 0-.5-1-.3-.8-.7-2-1.6-3.5-1-1.5-2-2.7-3-3.8-2.2-2.8-3.9-5-3.9-8.8C1 4.9 5 1 10 1s9 4 9 8.9c0 3.9-1.8 6-4 8.8-1 1.2-1.9 2.4-2.8 3.8-1 1.5-1.4 2.7-1.6 3.5-.3 1-.4 1-.6 1Z',
    fillOpacity: 1,
    strokeWeight: 1,
    anchor: new google.maps.Point(15, 29),
    scale: 1.2,
    labelOrigin: new google.maps.Point(10, 9),
  };
  const originMarkerIcon = {
    ...markerIconConfig,
    fillColor: MARKER_ICON_COLORS.active.fill,
    strokeColor: MARKER_ICON_COLORS.active.stroke,
  };
  const destinationMarkerIcon = {
    ...markerIconConfig,
    fillColor: MARKER_ICON_COLORS.inactive.fill,
    strokeColor: MARKER_ICON_COLORS.inactive.stroke,
  };
  // const bikeLayer = new google.maps.BicyclingLayer();
  // const publicTransitLayer = new google.maps.TransitLayer();

  initMapView();
  initDestinations();
  initCommutesPanel();
  initCommutesModal();

  /**
   * Initializes map view on commutes widget.
   */
  function initMapView() {
    const mapOptionConfig = configuration.mapOptions;
    commutesMap = new google.maps.Map(commutesEl.map, mapOptionConfig);

    configuration.defaultTravelModeEnum = TravelMode.DRIVING;
    //parseTravelModeEnum(configuration.defaultTravelMode);
    //setTravelModeLayer(configuration.defaultTravelModeEnum);
    createMarker(origin);
  }

  /**
   * Initializes commutes widget with destinations info if provided with a list
   * of initial destinations and update view.
   */
  function initDestinations() {
    if (!configuration.initialDestinations) return;
    let callbackCounter = 0;
    const placesService = new google.maps.places.PlacesService(commutesMap);
    for (const destination of configuration.initialDestinations) {
      destination.travelModeEnum = TravelMode.DRIVING;
      // parseTravelModeEnum(destination.travelMode);
      const label = getNextMarkerLabel();
      const request = {
        placeId: destination.placeId,
        fields: ['place_id', 'geometry', 'name'],
      };
      placesService.getDetails(
        request,
        function (place) {
          if (!place.geometry || !place.geometry.location) return;
          const travelModeEnum =
            destination.travelModeEnum || configuration.defaultTravelModeEnum;
          const destinationConfig =
            createDestinationConfig(place, travelModeEnum, label);
          getDirections(destinationConfig).then((response) => {
            if (!response) return;
            destinations.push(destinationConfig);
            getCommutesInfo(response, destinationConfig);
            callbackCounter++;
            // Update commutes panel and click event objects after getting
            // direction to all destinations.
            if (callbackCounter === configuration.initialDestinations.length) {
              destinations.sort(function (a, b) {
                return a.label < b.label ? -1 : 1;
              });
              let bounds = new google.maps.LatLngBounds();
              for (let i = 0; i < destinations.length; i++) {
                assignMapObjectListeners(destinations[i], i);
                updateCommutesPanel(destinations[i], i, DestinationOperation.ADD);
                bounds.union(destinations[i].bounds);
              }
              const lastIndex = destinations.length - 1;
              handleRouteClick(destinations[lastIndex], lastIndex);
              commutesMap.fitBounds(bounds);
              console.log(destinations)
            }
          });
        },
        () => {
          console.error('Failed to retrieve places info due to ' + e);
        });
    }
  }

  /**
   * Initializes the bottom panel for updating map view and displaying commutes
   * info.
   */
  function initCommutesPanel() {
    const addCommutesButtonEls = document.querySelectorAll('.add-button');
    addCommutesButtonEls.forEach(addButton => {
      addButton.addEventListener('click', () => {
        destinationModalEl.title.innerHTML = 'Add destination';
        hideElement(destinationModalEl.deleteButton);
        hideElement(destinationModalEl.editButton);
        showElement(destinationModalEl.addButton);
        showModal();
        const travelModeEnum = configuration.defaultTravelModeEnum || TravelMode.DRIVING;
        const travelModeId = travelModeEnum.toLowerCase() + '-mode';
        document.forms['destination-form'][travelModeId].checked = true;
      });
    });

    destinationPanelEl.scrollLeftButton.addEventListener(
      'click', handleScrollButtonClick);
    destinationPanelEl.scrollRightButton.addEventListener(
      'click', handleScrollButtonClick);
    destinationPanelEl.list.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' &&
        e.target !== destinationPanelEl.getActiveDestination()) {
        e.target.click();
        e.preventDefault();
      }
    });
  }

  /**
   * Initializes commutes modal to gathering destination inputs. Configures the
   * event target listeners to update view and behaviors on the modal.
   */
  function initCommutesModal() {
    const boundConfig = {
      north: origin.lat + BIAS_BOUND_DISTANCE,
      south: origin.lat - BIAS_BOUND_DISTANCE,
      east: origin.lng + BIAS_BOUND_DISTANCE,
      west: origin.lng - BIAS_BOUND_DISTANCE,
    };

    const destinationFormReset = function () {
      destinationModalEl.destinationInput.classList.remove('error');
      destinationModalEl.errorMessage.innerHTML = '';
      destinationModalEl.form.reset();
      destinationToAdd = null;
    };

    const autocompleteOptions = {
      bounds: boundConfig,
      fields: ['place_id', 'geometry', 'name'],
    };
    const autocomplete = new google.maps.places.Autocomplete(
      destinationModalEl.destinationInput, autocompleteOptions);
    let destinationToAdd;
    autocomplete.addListener('place_changed', () => {
      const place = autocomplete.getPlace();
      if (!place.geometry || !place.geometry.location) {
        return;
      } else {
        destinationToAdd = place;
        destinationModalEl.getTravelModeInput().focus();
      }
      destinationModalEl.destinationInput.classList.remove('error');
      destinationModalEl.errorMessage.innerHTML = '';
    });

    destinationModalEl.addButton.addEventListener('click', () => {
      const isValidInput = validateDestinationInput(destinationToAdd);
      if (!isValidInput) return;
      const selectedTravelMode = destinationModalEl.getTravelModeInput().value;
      addDestinationToList(destinationToAdd, selectedTravelMode);
      destinationFormReset();
      hideModal();
    });

    destinationModalEl.editButton.addEventListener('click', () => {
      const destination = { ...destinations[activeDestinationIndex] };
      const selectedTravelMode = destinationModalEl.getTravelModeInput().value;
      const isSameDestination =
        destination.name === destinationModalEl.destinationInput.value;
      const isSameTravelMode = destination.travelModeEnum === selectedTravelMode;
      if (isSameDestination && isSameTravelMode) {
        hideModal();
        return;
      }
      if (!isSameDestination) {
        const isValidInput = validateDestinationInput(destinationToAdd);
        if (!isValidInput) return;
        destination.name = destinationToAdd.name;
        destination.place_id = destinationToAdd.place_id;
        destination.url = generateMapsUrl(destinationToAdd, selectedTravelMode);
      }
      if (!isSameTravelMode) {
        destination.travelModeEnum = selectedTravelMode;
        destination.url = generateMapsUrl(destination, selectedTravelMode);
      }
      destinationFormReset();
      getDirections(destination)
        .then((response) => {
          if (!response) return;
          const currentIndex = activeDestinationIndex;
          // Remove current active direction before replacing it with updated
          // routes.
          removeDirectionsFromMapView(destination);
          destinations[activeDestinationIndex] = destination;
          getCommutesInfo(response, destination);
          assignMapObjectListeners(destination, activeDestinationIndex);
          updateCommutesPanel(
            destination, activeDestinationIndex, DestinationOperation.EDIT);
          handleRouteClick(destination, activeDestinationIndex);
          const newEditButton = destinationPanelEl.list.children
            .item(activeDestinationIndex)
            .querySelector('.edit-button');
          newEditButton.focus();
        })
        .catch((e) => console.error('Editing directions failed due to ' + e));
      hideModal();
    });

    destinationModalEl.cancelButton.addEventListener('click', () => {
      destinationFormReset();
      hideModal();
    });

    destinationModalEl.deleteButton.addEventListener('click', () => {
      removeDirectionsFromMapView(destinations[activeDestinationIndex]);
      updateCommutesPanel(
        destinations[activeDestinationIndex], activeDestinationIndex,
        DestinationOperation.DELETE);
      activeDestinationIndex = undefined;
      destinationFormReset();
      let elToFocus;
      if (destinations.length) {
        const lastIndex = destinations.length - 1;
        handleRouteClick(destinations[lastIndex], lastIndex);
        elToFocus = destinationPanelEl.getActiveDestination();
      } else {
        elToFocus = commutesEl.initialStatePanel.querySelector('.add-button');
      }
      hideModal(elToFocus);
    });

    window.onmousedown = function (event) {
      if (event.target === commutesEl.modal) {
        destinationFormReset();
        hideModal();
      }
    };

    commutesEl.modal.addEventListener('keydown', (e) => {
      switch (e.key) {
        case 'Enter':
          if (e.target === destinationModalEl.cancelButton ||
            e.target === destinationModalEl.deleteButton) {
            return;
          }
          if (destinationModalEl.addButton.style.display !== 'none') {
            destinationModalEl.addButton.click();
          } else if (destinationModalEl.editButton.style.display !== 'none') {
            destinationModalEl.editButton.click();
          }
          break;
        case "Esc":
        case "Escape":
          hideModal();
          break;
        default:
          return;
      }
      e.preventDefault();
    });

    // Trap focus in the modal so that tabbing on the last interactive element
    // focuses on the first, and shift-tabbing on the first interactive element
    // focuses on the last.

    const firstInteractiveElement = destinationModalEl.destinationInput;
    const lastInteractiveElements = [
      destinationModalEl.addButton,
      destinationModalEl.editButton,
    ];

    firstInteractiveElement.addEventListener(
      'keydown', handleFirstInteractiveElementTab);
    for (const el of lastInteractiveElements) {
      el.addEventListener('keydown', handleLastInteractiveElementTab);
    }

    function handleFirstInteractiveElementTab(event) {
      if (event.key === 'Tab' && event.shiftKey) {
        for (const el of lastInteractiveElements) {
          if (el.style.display !== 'none') {
            event.preventDefault();
            el.focus();
            return;
          }
        }
      }
    }

    function handleLastInteractiveElementTab(event) {
      if (event.key === 'Tab' && !event.shiftKey) {
        event.preventDefault();
        firstInteractiveElement.focus();
      }
    }
  }

  /**
   * Checks if destination input is valid and ensure no duplicate places or more
   * than max number places are added.
   */
  function validateDestinationInput(destinationToAdd) {
    let errorMessage;
    let isValidInput = false;
    if (!destinationToAdd) {
      errorMessage = 'No details available for destination input';
    } else if (destinations.length > MAX_NUM_DESTINATIONS) {
      errorMessage =
        'Cannot add more than ' + MAX_NUM_DESTINATIONS + ' destinations';
    } else if (
      destinations &&
      destinations.find(
        destination =>
          destination.place_id === destinationToAdd.place_id)) {
      errorMessage = 'Destination is already added';
    } else {
      isValidInput = true;
    }
    if (!isValidInput) {
      destinationModalEl.errorMessage.innerHTML = errorMessage;
      destinationModalEl.destinationInput.classList.add('error');
    }
    return isValidInput;
  }

  /**
   * Removes polylines and markers of currently active directions.
   */
  function removeDirectionsFromMapView(destination) {
    destination.polylines.innerStroke.setMap(null);
    destination.polylines.outerStroke.setMap(null);
    destination.marker.setMap(null);
  }

  /**
   * Generates destination card template, attach event target listeners, and
   * adds template to destination list depending on the operations:
   * - add new destination card template to the end of the list on add.
   * - replace destination card template for current selected on edit.
   * - do nothing on default or delete.
   */
  function buildDestinationCardTemplate(
    destination, destinationIdx, destinationOperation) {
    let editButtonEl;
    switch (destinationOperation) {
      case DestinationOperation.ADD:
        destinationPanelEl.list.insertAdjacentHTML(
          'beforeend',
          '<div class="destination-container">' +
          generateDestinationTemplate(destination) + '</div>');
        const destinationContainerEl = destinationPanelEl.list.lastElementChild;
        destinationContainerEl.addEventListener('click', () => {
          handleRouteClick(destination, destinationIdx);
        });
        editButtonEl = destinationContainerEl.querySelector('.edit-button');
        destinationPanelEl.container.scrollLeft =
          destinationPanelEl.container.scrollWidth;
        break;
      case DestinationOperation.EDIT:
        const activeDestinationContainerEl =
          destinationPanelEl.getActiveDestination().parentElement;
        activeDestinationContainerEl.innerHTML = generateDestinationTemplate(destination);
        activeDestinationContainerEl.addEventListener('click', () => {
          handleRouteClick(destination, destinationIdx);
        });
        editButtonEl = activeDestinationContainerEl.querySelector('.edit-button');
        break;
      case DestinationOperation.DELETE:
      default:
    }

    editButtonEl.addEventListener('click', () => {
      destinationModalEl.title.innerHTML = 'Edit destination';
      destinationModalEl.destinationInput.value = destination.name;
      showElement(destinationModalEl.deleteButton);
      showElement(destinationModalEl.editButton);
      hideElement(destinationModalEl.addButton);
      showModal();
      const travelModeId = destination.travelModeEnum.toLowerCase() + '-mode';
      document.forms['destination-form'][travelModeId].checked = true;
      // Update the autocomplete widget as if it was user input.
      destinationModalEl.destinationInput.dispatchEvent(new Event('input'));
    });
  }

  /**
   * Updates view of commutes panel depending on the operation:
   * - build/update destination template if add or edit.
   * - remove destination from destination list and rebuild template.
   */
  function updateCommutesPanel(
    destination, destinationIdx, destinationOperation) {
    switch (destinationOperation) {
      case DestinationOperation.ADD:
        hideElement(commutesEl.initialStatePanel);
        showElement(commutesEl.destinationPanel);
      // fall through
      case DestinationOperation.EDIT:
        buildDestinationCardTemplate(
          destination, destinationIdx, destinationOperation);
        break;
      case DestinationOperation.DELETE:
        destinations.splice(destinationIdx, 1);
        destinationPanelEl.list.innerHTML = '';
        for (let i = 0; i < destinations.length; i++) {
          buildDestinationCardTemplate(
            destinations[i], i, DestinationOperation.ADD);
          assignMapObjectListeners(destinations[i], i);
        }
      default:
    }
    if (!destinations.length) {
      showElement(commutesEl.initialStatePanel, commutesEl.initialStatePanel);
      hideElement(commutesEl.destinationPanel);
      activeDestinationIndex = undefined;
      setStateGenerateRouteButton(true); 
      return;
    }
    destinationPanelEl.container.addEventListener('scroll', handlePanelScroll);
    destinationPanelEl.container.dispatchEvent(new Event('scroll'));
    setStateGenerateRouteButton(false);  
  }

  /**
   * Adds new destination to the list and get directions and commutes info.
   */
  function addDestinationToList(destinationToAdd, travelModeEnum) {
    const destinationConfig =
      createDestinationConfig(destinationToAdd, travelModeEnum);
    const newDestinationIndex = destinations.length;
    getDirections(destinationConfig)
      .then((response) => {
        if (!response) return;
        destinations.push(destinationConfig);
        getCommutesInfo(response, destinationConfig);
        assignMapObjectListeners(destinationConfig, newDestinationIndex);
        updateCommutesPanel(
          destinationConfig, newDestinationIndex, DestinationOperation.ADD);
        handleRouteClick(destinationConfig, newDestinationIndex);
        destinationPanelEl.addButton.focus();
      })
      .catch((e) => console.error('Adding destination failed due to ' + e));
  }

  /**
   * Returns a new marker label on each call. Marker labels are the capital
   * letters of the alphabet in order.
   */
  function getNextMarkerLabel() {
    const markerLabels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const label = markerLabels[markerIndex];
    markerIndex = (markerIndex + 1) % markerLabels.length;
    return label;
  }

  /**
   * Creates a destination config object from the given data. The label argument
   * is optional; a new label will be generated if not provided.
   */
  function createDestinationConfig(destinationToAdd, travelModeEnum, label) {
    return {
      name: destinationToAdd.name,
      place_id: destinationToAdd.place_id,
      label: label || getNextMarkerLabel(),
      travelModeEnum: travelModeEnum,
      url: generateMapsUrl(destinationToAdd, travelModeEnum),
    };
  }

  /**
   * Gets directions to destination from origin, add route to map view, and
   * update commutes panel with distance and directions info.
   */
  function getDirections(destination) {
    const request = {
      origin: origin,
      destination: { 'placeId': destination.place_id },
      travelMode: destination.travelModeEnum,
      unitSystem: configuration.distanceMeasurementType === 'METRIC' ?
        google.maps.UnitSystem.METRIC : google.maps.UnitSystem.IMPERIAL,
    };
    const directionsService = new google.maps.DirectionsService();
    return directionsService.route(request).then(response => {
      return response;
    });
  }

  /**
   * Adds route polyline, marker, and commutes info to map and destinations
   * list.
   */
  function getCommutesInfo(directionResponse, destination) {
    if (!directionResponse) return;
    const path = directionResponse.routes[0].overview_path;
    const bounds = directionResponse.routes[0].bounds;
    const directionLeg = directionResponse.routes[0].legs[0];
    const destinationLocation = directionLeg.end_location;
    const distance = directionLeg.distance.text;
    const duration = convertDurationValueAsString(directionLeg.duration.value);

    const innerStroke = new google.maps.Polyline({
      path: path,
      strokeColor: STROKE_COLORS.inactive.innerStroke,
      strokeOpacity: 1.0,
      strokeWeight: 3,
      zIndex: 10
    });

    const outerStroke = new google.maps.Polyline({
      path: path,
      strokeColor: STROKE_COLORS.inactive.outerStroke,
      strokeOpacity: 1.0,
      strokeWeight: 6,
      zIndex: 1
    });

    const marker = createMarker(destinationLocation, destination.label);

    innerStroke.setMap(commutesMap);
    outerStroke.setMap(commutesMap);

    destination.distance = distance;
    destination.duration = duration;
    destination.marker = marker;
    destination.polylines = { innerStroke, outerStroke };
    destination.bounds = bounds;
  }

  /**
   * Assigns event target listeners to map objects of corresponding destination
   * index.
   */
  function assignMapObjectListeners(destination, destinationIdx) {
    google.maps.event.clearListeners(destination.marker, 'click');

    google.maps.event.addListener(destination.marker, 'click', () => {
      handleRouteClick(destination, destinationIdx);
      destinationPanelEl.list.querySelectorAll('.destination')[destinationIdx].focus();
    });
    google.maps.event.addListener(destination.marker, 'mouseover', () => {
      changeMapObjectStrokeWeight(destination, true);
    });
    google.maps.event.addListener(destination.marker, 'mouseout', () => {
      changeMapObjectStrokeWeight(destination, false);
    });
    for (const strokeLine in destination.polylines) {
      google.maps.event.clearListeners(destination.polylines[strokeLine], 'click');
      google.maps.event.clearListeners(destination.polylines[strokeLine], 'mouseover');

      google.maps.event.addListener(destination.polylines[strokeLine], 'click', () => {
        handleRouteClick(destination, destinationIdx);
        destinationPanelEl.list.querySelectorAll('.destination')[destinationIdx].focus();
      });
      google.maps.event.addListener(destination.polylines[strokeLine], 'mouseover', () => {
        changeMapObjectStrokeWeight(destination, true);
      });
      google.maps.event.addListener(destination.polylines[strokeLine], 'mouseout', () => {
        changeMapObjectStrokeWeight(destination, false);
      });
    }
  }

  /**
   * Generates the Google Map url for direction from origin to destination with
   * corresponding travel mode.
   */
  function generateMapsUrl(destination, travelModeEnum) {
    let googleMapsUrl = 'https://www.google.com/maps/dir/?api=1';
    googleMapsUrl += `&origin=${origin.lat},${origin.lng}`;
    googleMapsUrl += '&destination=' + encodeURIComponent(destination.name) +
      '&destination_place_id=' + destination.place_id;
    googleMapsUrl += '&travelmode=' + travelModeEnum.toLowerCase();
    return googleMapsUrl;
  }

  /**
   * Handles changes to destination polyline and map icon stroke weight.
   */
  function changeMapObjectStrokeWeight(destination, mouseOver) {
    const destinationMarkerIcon = destination.marker.icon;
    if (mouseOver) {
      destination.polylines.outerStroke.setOptions({ strokeWeight: 8 });
      destinationMarkerIcon.strokeWeight = 2;
      destination.marker.setIcon(destinationMarkerIcon);
    }
    else {
      destination.polylines.outerStroke.setOptions({ strokeWeight: 6 });
      destinationMarkerIcon.strokeWeight = 1;
      destination.marker.setIcon(destinationMarkerIcon);
    }
  }

  /**
   * Handles route clicks. Originally active routes are set to inactive
   * states. Newly selected route's map polyline/marker objects and destination
   * template are assigned active class styling and coloring.
   */
  function handleRouteClick(destination, destinationIdx) {
    if (activeDestinationIndex !== undefined) {
      // Set currently active stroke to inactive
      destinations[activeDestinationIndex].polylines.innerStroke.setOptions(
        { strokeColor: STROKE_COLORS.inactive.innerStroke, zIndex: 2 });
      destinations[activeDestinationIndex].polylines.outerStroke.setOptions(
        { strokeColor: STROKE_COLORS.inactive.outerStroke, zIndex: 1 });

      // Set current active marker to grey
      destinations[activeDestinationIndex].marker.setIcon(
        destinationMarkerIcon);
      destinations[activeDestinationIndex].marker.label.color =
        MARKER_ICON_COLORS.inactive.label;

      // Remove styling of current active destination.
      const activeDestinationEl = destinationPanelEl.getActiveDestination();
      if (activeDestinationEl) {
        activeDestinationEl.classList.remove('active');
      }
    }

    activeDestinationIndex = destinationIdx;

    // setTravelModeLayer(destination.travelModeEnum);
    // Add active class
    const newDestinationEl = destinationPanelEl.list.querySelectorAll(
      '.destination')[destinationIdx];
    newDestinationEl.classList.add('active');
    // Scroll into view
    newDestinationEl.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Make line active
    destination.polylines.innerStroke.setOptions(
      { strokeColor: STROKE_COLORS.active.innerStroke, zIndex: 101 });
    destination.polylines.outerStroke.setOptions(
      { strokeColor: STROKE_COLORS.active.outerStroke, zIndex: 99 });

    destination.marker.setIcon(originMarkerIcon);
    destination.marker.label.color = '#ffffff';

    commutesMap.fitBounds(destination.bounds);
  }

  /**
   * Generates new marker based on location and label.
   */
  function createMarker(location, label) {
    const isOrigin = label === undefined ? true : false;
    const markerIconConfig = isOrigin ? originMarkerIcon : destinationMarkerIcon;
    const labelColor = isOrigin ? MARKER_ICON_COLORS.active.label :
      MARKER_ICON_COLORS.inactive.label;
    const labelText = isOrigin ? '●' : label;

    const mapOptions = {
      position: location,
      map: commutesMap,
      label: {
        text: labelText,
        fontFamily: 'Arial, sans-serif',
        color: labelColor,
        fontSize: '16px',
      },
      icon: markerIconConfig
    };

    if (isOrigin) {
      mapOptions.label.className += ' origin-pin-label';
      mapOptions.label.fontSize = '20px';
    }
    const marker = new google.maps.Marker(mapOptions);

    return marker;
  }

  /**
  * Returns a TravelMode enum parsed from the input string, or null if no match is found.
  
  function parseTravelModeEnum(travelModeString) {
    switch (travelModeString) {
      case 'DRIVING':
        return TravelMode.DRIVING;
      case 'BICYCLING':
        return TravelMode.BICYCLING;
      case 'PUBLIC_TRANSIT':
        return TravelMode.TRANSIT;
      case 'WALKING':
        return TravelMode.WALKING;
      default:
        return null;
    }
  }
  */

  /**
   * Sets map layer depending on the chosen travel mode.
  function setTravelModeLayer(travelModeEnum) {
    switch (travelModeEnum) {
      case TravelMode.BICYCLING:
        publicTransitLayer.setMap(null);
        bikeLayer.setMap(commutesMap);
        break;
        case TravelMode.TRANSIT:
          bikeLayer.setMap(null);
          publicTransitLayer.setMap(commutesMap);
          break;
          default:
            publicTransitLayer.setMap(null);
            bikeLayer.setMap(null);
          }
        }
        
  */

  /**
   * Convert time from durationValue in seconds into readable string text.
   */
  function convertDurationValueAsString(durationValue) {
    if (!durationValue) {
      return '';
    }
    if (durationValue < MIN_IN_SECONDS) {
      return '<1 min';
    }
    if (durationValue > HOUR_IN_SECONDS * 10) {
      return '10+ hours';
    }
    const hours = Math.floor(durationValue / HOUR_IN_SECONDS);
    const minutes = Math.floor(durationValue % HOUR_IN_SECONDS / 60);
    const hoursString = hours > 0 ? hours + ' h' : '';
    const minutesString = minutes > 0 ? minutes + ' min' : '';
    const spacer = hoursString && minutesString ? ' ' : '';
    return hoursString + spacer + minutesString;
  }

  /**
   * Shows the destination modal window, saving a reference to the currently
   * focused element so that focus can be restored by hideModal().
   */
  function showModal() {
    lastActiveEl = document.activeElement;
    showElement(commutesEl.modal, destinationModalEl.destinationInput);
  }

  /**
   * Hides the destination modal window, setting focus to focusEl if provided.
   * If no argument is passed, focus is restored to where it was when
   * showModal() was called.
   */
  function hideModal(focusEl) {
    hideElement(commutesEl.modal, focusEl || lastActiveEl);
  }
}

/**
 * Hides a DOM element and optionally focuses on focusEl.
 */
function hideElement(el, focusEl) {
  el.style.display = 'none';
  if (focusEl) focusEl.focus();
}

/**
 * Shows a DOM element that has been hidden and optionally focuses on focusEl.
 */
function showElement(el, focusEl) {
  el.style.display = 'flex';
  if (focusEl) focusEl.focus();
}

/**
 * Event handler function for scroll buttons.
 */
function handleScrollButtonClick(e) {
  const multiplier = 1.25;
  const direction = e.target.dataset.direction;
  const cardWidth = destinationPanelEl.list.firstElementChild.offsetWidth;

  destinationPanelEl.container.scrollBy(
    { left: (direction * cardWidth * multiplier), behavior: 'smooth' });
}

/**
 * Event handler on scroll to add scroll buttons only if scroll width is larger
 * than width. Hide scroll buttons if scrolled to the start or end of the panel.
 */
function handlePanelScroll() {
  const position = destinationPanelEl.container.scrollLeft;
  const scrollWidth = destinationPanelEl.container.scrollWidth;
  const width = destinationPanelEl.container.offsetWidth;

  if (scrollWidth > width) {
    if (position === 0) {
      destinationPanelEl.scrollLeftButton.classList.remove('visible');
    } else {
      destinationPanelEl.scrollLeftButton.classList.add('visible');
    }

    if (Math.ceil(position + width) >= scrollWidth) {
      destinationPanelEl.scrollRightButton.classList.remove('visible');
    } else {
      destinationPanelEl.scrollRightButton.classList.add('visible');
    }
  }
}

/**
 * Generates new destination template based on destination info properties.
 */
function generateDestinationTemplate(destination) {
  const travelModeIconTemplate = '<use href="#commutes-' +
    destination.travelModeEnum.toLowerCase() + '-icon"/>';
  return `
    <div class="destination" tabindex="0" role="button">
      <div class="destination-content">
        <div class="metadata">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              ${travelModeIconTemplate}
          </svg>
          ${destination.distance}
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <use href="#commutes-arrow-icon"/>
          </svg>
          <span class="location-marker">${destination.label}</span>
        </div>
        <div class="address">To
          <abbr title="${destination.name}">${destination.name}</abbr>
        </div>
        <div class="destination-eta">${destination.duration}</div>
      </div>
    </div>

    <div class="destination-controls">
      <a class="directions-button" href=${destination.url} target="_blank"
         aria-label="Link to directions in Google Maps">
        <svg aria-label="Directions icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <use href="#commutes-directions-icon"/>
        </svg>
      </a>
      <button class="edit-button" aria-label="Edit Destination">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <use href="#commutes-edit-icon"/>
        </svg>
        Edit
      </button>
    </div>`;
}