

$( document ).ready(function() {
	if ($( "#map_input" ).length ) {
	$( "#map_input" ).parent().after('<div id="mapeditorview" style="height:400px"></div>');
	
    $( "#p_acres" ).text(Math.round($("#map_acres").val()));

	
	var drawnItems = new L.FeatureGroup();
	
	
	

	
	// create a map in the "map" div, set the view to a given place and zoom
	var map = L.map('mapeditorview').setView([53, -100], 4);


	
	var gmap_layer = new L.Google('HYBRID');
	map.addLayer(gmap_layer);
	
	if ($( "#map_input" ).val()) {
			drawnItems = L.geoJson( jQuery.parseJSON( $( "#map_input" ).val() ) );
			map.fitBounds(drawnItems.getBounds());
		}
	
			map.addLayer(drawnItems);
			
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
		
		
			map.addControl(drawControl);
			
			map.on('draw:created', function (e) {
			    var type = e.layerType,
			        layer = e.layer;

			    		drawnItems.addLayer(layer);
							
			    		var geojson = layer.toGeoJSON();
			    		var acres = calculateArea(geojson.features[0]);
							
						$("#map_acres").val(acres);
						$( "#map_input" ).val( JSON.stringify( geojson ) );
                        $( "#p_acres" ).text(Math.round(acres));
					
			});	
			
			map.on('draw:editstop', function () {
				$( "#map_input" ).val( JSON.stringify( drawnItems.toGeoJSON() ) );

				var geojson = drawnItems.toGeoJSON();
				var acres = calculateArea(geojson.features[0]);

			    $("#map_acres").val(acres);
                $("#map_input").val( JSON.stringify( geojson ) );
                $( "#p_acres" ).text(Math.round(acres));
			});	
			
				
		}
			
});

function calculateArea(geojson) {
    var path = new Array();
		var coordinate = geojson.geometry.coordinates[0];

    coordinate.forEach( function(c) {
    	path.push(new google.maps.LatLng(c[1], c[0]));
		});

    var area_m2 = google.maps.geometry.spherical.computeArea(path);
    var acres = area_m2 * 0.000247105;
		
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
		
		
		var gmap_layer = new L.Google('HYBRID');
		map.addLayer(gmap_layer);
		
		l = L.geoJson(geo).addTo(map);
		
		map.fitBounds(l.getBounds());
			
	});
	
	
}

