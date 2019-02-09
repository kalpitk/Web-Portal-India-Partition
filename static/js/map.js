/* Add this to HTML template
 * <script> const coordinates = {{res|tojson|safe}}; </script>
 * where res stores the co-ordinates selected from db
 */
var map;
function addMarker(coord) {
    var marker1 = new google.maps.Marker({
        position: {lat:coord[0], lng:coord[1]},
        map:map
    });
    var marker2 = new google.maps.Marker({
        position: {lat:coord[2], lng:coord[3]},
        map:map
    });
    var path = new google.maps.Polyline({
        map: map,
        path: [{lat:coord[0], lng:coord[1]}, {lat:coord[2], lng:coord[3]}],
        geodesic: false,
        strokeColor: 'red',
        strokeOpacity: 1.0,
        strokeWeight: 5
    });
    path.addListener('click', function () {
        alert('path clicked');
    });
    marker1.addListener('click', function () {
        alert('source clicked');
    });
    marker2.addListener('click', function () {
        alert('destination clicked');
    });
}
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
    });
    const len = coordinates.length;
    console.log(len);
    for(var i=0;i<len;i++) {
        addMarker(coordinates[i]);
    }
}
