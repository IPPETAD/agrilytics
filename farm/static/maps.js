

$( document ).ready(function() {
	$( "#map_input" ).parent().after('<div id="mapview" style="height:400px"></div>');
	
	
	var drawnItems = new L.FeatureGroup();
	
	
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
	        edit: false
	    }
	});
	
	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('mapview').setView([53, -100], 4);

	// add an OpenStreetMap tile layer
	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);
	map.addControl(drawControl);
	map.addLayer(drawnItems);
			
			
			map.on('draw:created', function (e) {
			    var type = e.layerType,
			        layer = e.layer;
							
							console.log( layer.toGeoJSON() );

			    drawnItems.addLayer(layer);
					
					$( "#map_input" ).val( JSON.stringify( layer.toGeoJSON() ) );
			});		
			
			
});



