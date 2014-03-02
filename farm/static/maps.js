

$( document ).ready(function() {
	if ($( "#map_input" ).length ) {
	$( "#map_input" ).parent().after('<div id="mapeditorview" style="height:400px"></div>');
	
	


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
					
					$( "#map_input" ).val( JSON.stringify( layer.toGeoJSON() ) );
			});	
			
			map.on('draw:editstop', function (e) {
			    var type = e.layerType,
			        layer = e.layer;
					
					$( "#map_input" ).val( JSON.stringify( layer.toGeoJSON() ) );
			});	
				
		}
			
});



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

