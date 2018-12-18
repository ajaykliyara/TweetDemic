/*  This visualization was made possible by modifying code provided by:

Scott Murray, Choropleth example from "Interactive Data Visualization for the Web"
https://github.com/alignedleft/d3-book/blob/master/chapter_12/05_choropleth.html

Malcolm Maclean, tooltips example tutorial
http://www.d3noob.org/2013/01/adding-tooltips-to-d3js-graph.html

Mike Bostock, Pie Chart Legend
http://bl.ocks.org/mbostock/3888852  */



//Width and height of map
var width = 540;
var height = 350;

// D3 Projection
var projection = d3.geoAlbersUsa()
				   .translate([width/2, height/2])    // translate to center of screen
				   .scale([700]);          // scale things down so see entire US

// Define path generator
var path = d3.geoPath()               // path generator that will convert GeoJSON to SVG paths
		  	 .projection(projection);  // tell path generator to use albersUsa projection


// Define linear scale for output
//var color = d3.scaleLinear().range(["rgb(69,173,168)","rgb(84,36,55)","rgb(217,91,67)"]);

// Define linear scale for output
var color = d3.scaleOrdinal().domain([1,3]).range(["rgb(169,169,169)","rgb(69,173,168)","rgb(217,91,67)"]);

// parse the date / time
var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");

function checkIfToday(tweetDate)
{
	var today = new Date();
	var isToday = (today.toDateString() == tweetDate.toDateString());
	if (isToday)
	{
		return "orange";
	}
	else {
		return "white";
	}
}

//get color
function colorDimScale(sentiment)
{
	if (sentiment == "POSITIVE")
	{
		return color(3);
	}
	else if (sentiment == "NEGATIVE") {
		return color(2);
	}
	else {
		return color(1);
	}
}

var legendText = ["Negative", "Positive","Neutral"];

//Create SVG element and append map to the SVG
var svg = d3.select("body")
			.select('#band')
			.select(".right_charts")
			.select("#mapdiv")
			.append("svg")
			.attr("width", width)
			.attr("height", height);

// Append Div for tooltip to SVG
var div = d3.select("body").select('#band').select(".right_charts").select("#mapdiv")
		    .append("div")
    		.attr("class", "maptooltip")
    		.style("opacity", 0);

// Load in my states data!
//color.domain([0,1,2,3]); // setting the range of the input data
// Load GeoJSON data and merge with states data
d3.json("data/us-states.json", function(json) {


// Bind the data to the SVG and create one path per GeoJSON feature
svg.selectAll("path")
	.data(json.features)
	.enter()
	.append("path")
	.attr("d", path)
	.style("stroke", "#fff")
	.style("stroke-width", "1")
	.style("fill", "rgb(213,222,217)" );


// Map the cities I have lived in!
function drawMap(data){
//d3.csv("tweets.csv", function(data) {

	data.sort(function(a, b){
		return a["created_at_utc"]-b["created_at_utc"];
	});

	// format the data
  data.forEach(function(d) {
				d.lat = d.info.M.mapping_location.S.split(",")[1];
				d.lon = d.info.M.mapping_location.S.split(",")[0];
				d.sentiment_type = d.info.M.sentiment_type.S;
				d.sentiment_score = d.info.M.sentiment_score.S;
  });

svg.selectAll("circle")
	.data(data.filter(function(d) {
		return projection([d.lon, d.lat]) != null }
	)
)
	.enter()
	.append("a")
	.attr("xlink:href", function(d) { return "http://" + d.info.M.tweet_url.S; })
	.attr("target","_blank")
	.append("circle")
	.attr("cx", function(d) {
		return projection([d.lon, d.lat])[0];
	})
	.attr("cy", function(d) {
		return projection([d.lon, d.lat])[1];
	})
	.attr("r", function(d) {
		//return Math.sqrt(d.author_followers_count/10000) * 4;
		return 7;
	})
		.style("fill", function(d, i ) { return colorDimScale(d.sentiment_type); })
		.style("opacity", 0.85)
		.style("stroke", function(d, i) { return checkIfToday(d.created_at_utc); })
		.style("stroke-width", "2")
		//.style("stroke", "white")

	// Modification of custom tooltip code provided by Malcolm Maclean, "D3 Tips and Tricks"
	// http://www.d3noob.org/2013/01/adding-tooltips-to-d3js-graph.html
	.on("mouseover", function(d) {
    	div.transition()
      	   .duration(200)
           .style("opacity", .9);

           //div.text(d.info.M.tweet_text.S)
					 div.html(d.info.M.tweet_text.S + "<br/>" + "<b><i>" + d.created_at_local + "</i></b>" )
					 .style("left", (d3.event.pageX-document.getElementById('navTopVr1').offsetLeft+2) + "px")
					 .style("top", (d3.event.pageY-document.getElementById('navTopVr1').offsetTop-document.getElementById('right_charts').offsetTop - 28) + "px");

	})

    // fade out tooltip on mouse out
    .on("mouseout", function(d) {
        div.transition()
           .duration(500)
           .style("opacity", 0);
    });
//});
};
drawMap(wegmans_tweets_detail_data);

// Modified Legend Code from Mike Bostock: http://bl.ocks.org/mbostock/3888852
var legend = d3.select("body").select('#band').select(".right_charts").select("#mapdiv").append("svg")
      			.attr("class", "maplegend")
     			.attr("width", 140)
    			.attr("height", 200)
   				.selectAll("g")
   				.data(color.domain().slice().reverse())
   				.enter()
   				.append("g")
     			.attr("transform", function(d, i) { return "translate(40," + i * 20 + ")"; });

  	legend.append("rect")
   		  .attr("width", 18)
   		  .attr("height", 18)
   		  .style("fill", color);

  	legend.append("text")
  		  .data(legendText)
      	  .attr("x", 24)
      	  .attr("y", 9)
      	  .attr("dy", ".35em")
      	  .text(function(d) { return d; });

});
