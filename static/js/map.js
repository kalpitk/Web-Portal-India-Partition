var coordinates = new Array();
coordinates.push([{lat: -34.397, lng: 150.644},{lat: -33.397, lng: 149.644}]);
var map;
function addMarker(coord) {
    var marker1 = new google.maps.Marker({
        position: coord[0],
        map:map
    });
    var marker2 = new google.maps.Marker({
        position: coord[1],
        map:map
    });
    var path = new google.maps.Polyline({
        map: map,
        path: coord,
        geodesic: false,
        strokeColor: 'red',
        strokeOpacity: 1.0,
        strokeWeight: 5
    })
    path.addListener('click', function () {
        alert('path clicked');
    })
    marker1.addListener('click', function () {
        alert('source clicked');
    })
    marker2.addListener('click', function () {
        alert('destination clicked');
    })
    console.log('DONE');
}
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    });
    addMarker(coordinates[0]);
}
