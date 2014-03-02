

var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y/%m").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.month); })
    .y(function(d) { return y(d.price); });

function redraw() {	
			
		y.domain([0, d3.extent(window.data, function(d) { return d.price; })[1] ]);
		yAxis.scale(y);
				
		svg.select(".yaxis").transition().call(yAxis);
		
	var line = d3.svg.line()
	    .x(function(d) { return x(d.month); })
	    .y(function(d) { return y(d.price); });
			
			svg.selectAll('.line').datum(window.data);
			
			svg.selectAll('.line').transition().attr('d', line);
				
}
var svg;

$(document).ready( function() { 
svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
		.attr("viewBox", "0 0 960 500")
  	.attr("preserveAspectRatio", "xMidYMid")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

	

d3.json("/market/price_history?province=Alberta&crop=Rye", function(error, data) {
  data.forEach(function(d) {
    d.month = parseDate(d.month);
    d.price = +d.price;
  });
	
	window.data = data;
	
  x.domain(d3.extent(data, function(d) { return d.month; }));
  y.domain([0, d3.extent(data, function(d) { return d.price; })[1] ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis yaxis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Price ($/tonne)");

  svg.append("path")
      .datum(window.data)
      .attr("class", "line")
      .attr("d", line);
});



$(window).resize( function() {
	var aspect = 960 / 500;
	 chart = $("#chart svg");
    var targetWidth = chart.parent().width();
    chart.attr("width", targetWidth);
    chart.attr("height", targetWidth / aspect);
});

$(window).trigger('resize');
	
});
	
	
window.province = "Alberta";
window.crop = "Rye";
	
function reload(){
	newData(window.province, window.crop)
	
}
	
	function newData(province, crop) {
		
		d3.json("/market/price_history?province=" + province + "&crop=" + crop, function(error, data) {
		  data.forEach(function(d) {
		    d.month = parseDate(d.month);
		    d.price = +d.price;
		  })
			window.data = data;
			console.log(data);
			redraw();
		});
		
		
	}