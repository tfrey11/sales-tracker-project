let map;

async function initMap() {
    const position = { lat: 30.65537246306655, lng: -88.11527906790668 };
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    map = new Map(document.getElementById("dealer-map"), {
        zoom: 12,
        center: position,
        mapId: "Dealer Location"
    });

    const marker = new AdvancedMarkerElement({
        map: map,
        position: position,
        title: "BMW of Mobile"
    });

    
}

initMap();

