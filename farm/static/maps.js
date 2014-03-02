

$( document ).ready(function() {
	if ($( "#map_input" ).length ) {
	$( "#map_input" ).parent().after('<div id="mapeditorview" style="height:400px"></div>');
	$('#map_acres').prop('disabled', true);
	


	var drawnItems = new L.FeatureGroup();
	if ($( "#map_input" ).val()) {
			drawnItems = L.geoJson( jQuery.parseJSON( $( "#map_input" ).val() ) );
		}

	
	
	
	
	
	var drawControl = new L.Control.Draw({
	    draw: {
	        polygon: true,
	        marker: false,
					rectangle: false,
					polyline: false,
					circle: false
	    },
	    edit: {
	        featureGroup: drawnItems,
	        edit: true
	    }
	});
	
	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('mapeditorview').setView([53, -100], 4);


	map.addControl(drawControl);
	
	var gmap_layer = new L.Google('SATELLITE');
	map.addLayer(gmap_layer);
	
	
	map.addLayer(drawnItems);
	map.fitBounds(drawnItems.getBounds());
			
			
			map.on('draw:created', function (e) {
			    var type = e.layerType,
			        layer = e.layer;

			    drawnItems.addLayer(layer);
			    var geojson = layer.toGeoJSON();

			    $("#map_acres").val(calculateArea(geojson));
				$( "#map_input" ).val( JSON.stringify( geojson ) );
			});	
			
			map.on('draw:editstop', function (e) {
			    var type = e.layerType,
			        layer = e.layer;
				
			    var geojson = layer.toGeoJSON();

			    $("#map_acres").val(calculateArea(geojson));
				$( "#map_input" ).val( JSON.stringify( geojson ) );
			});	
				
		}
			
});

function calculateArea(geojson) {
    var path = new Array();
    for (var p in geojson.geometry.coordinates) {
        for (var c in p) {
            path.push(new google.maps.LatLng(c[1], c[0]));
        }
    }

    var area_m2 = google.maps.geometry.spherical.computeArea(path);
    var acres = area_m2 * 0.000247105;

    console.log('Calculated ares: ' + acres);
    return acres;
}


function loadStaticMap(geo){
	
	
	$( document ).ready(function() {
		// create a map in the "map" div, set the view to a given place and zoom
		var map = L.map('mapview').setView([53, -100], 4);

		// add an OpenStreetMap tile layer
		// L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		//     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
		// }).addTo(map);
		
		
		var gmap_layer = new L.Google('SATELLITE');
		map.addLayer(gmap_layer);
		
		l = L.geoJson(geo).addTo(map);
		
		map.fitBounds(l.getBounds());
			
	});
	
	
}

