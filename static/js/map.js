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
        window.open('/post_list?src_lat='+coord[0]+'&src_lng='+coord[1]+'&dest_lat='+coord[2]+'&dest_lng='+coord[3], '_self')
    });
    marker1.addListener('click', function () {
        window.open('/post_list?src_lat='+coord[0]+'&src_lng='+coord[1], '_self')
    });
    marker2.addListener('click', function () {
        window.open('/post_list?dest_lat='+coord[2]+'&dest_lng='+coord[3], '_self')
    });
}
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 28.62, lng: 73.27},
        zoom: 7
    });
    const len = coordinates.length;
    for(var i=0;i<len;i++) {
        addMarker(coordinates[i]);
    }
}
