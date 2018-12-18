

// set the dimensions and margins of the graph
var margin = {top: 40, right: 30, bottom: 30, left: 20},
    width = 760 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

// parse the date / time
var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

function drawScatter(data){
  data.sort(function(a, b){
    return a["created_at_utc"]-b["created_at_utc"];
  });

  // format the data
  data.forEach(function(d) {
      d.created_at_utc = parseTime(d.created_at_utc.S);
      d.created_at_local = new Date(d.created_at_utc.toLocaleString());
      d.author_followers_count = d.info.M.author_followers_count.S;
      d.sentiment_type = d.info.M.sentiment_type.S;
      d.sentiment_score = d.info.M.sentiment_score.S;

  });

  // Scale the range of the data
  x.domain(d3.extent(data, function(d) { return d.created_at_local; }));
  y.domain([40, d3.max(data, function(d) { return (d.sentiment_score*100)+10; })]);

  var colorScale = d3.scaleSequential(d3.interpolateInferno).domain([0, height])

  // Define linear scale for output
  var color = d3.scaleOrdinal().domain([1,3]).range(["rgb(192,192,192)","rgb(69,173,168)","rgb(217,91,67)"]);

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



  var svg = d3.select('body').select('#band').select(".left_charts").select("#scatter").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform","translate(" + margin.left + "," + '-10' + ")");

  // Add the scatterplot
  svg.selectAll("dot")
      .data(data)
      .enter()
      .append("a")
      .attr("xlink:href", function(d) { return "http://" + d.info.M.tweet_url.S; })
      .attr("target","_blank")
      .append("circle")
      //.filter(function(d) { return d.sentiment_type == "NEGATIVE" })
      .attr("class", "dot")
      //.attr("r", function(d){ return (Math.sqrt(d.author_followers_count *4/Math.PI)); })
      //.attr("r", function(d){ return 5; })
      .attr("r", function(d){ return Math.log(d.author_followers_count)*2; })
      .attr("cx", function(d) { return x(d.created_at_local); })
      .attr("cy", function(d) { return y(d.sentiment_score*100); })
      .style("stroke", "grey")
      .style("stroke-width", "2")
      .style("fill", function(d, i ) { return colorDimScale(d.sentiment_type); })
      .on("mouseover", function(d) {
          div.transition()
               .duration(200)
               .style("opacity", .9);

          div.html(d.info.M.tweet_text.S + "<br/>" + "<b><i>" + d.created_at_local + "</i></b>" );

      })
        // fade out tooltip on mouse out
        .on("mouseout", function(d) {
            div.transition()
               .duration(500)
               .style("opacity", 0);
        });

  // Add the X Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));


      // text label for the y axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -20)
        .attr("x",-800 / 2)
        .attr("dy", "2em")
        .style("text-anchor", "middle")
        .text("Sentiment Confidence %");

};

drawScatter(wegmans_tweets_detail_data);
