// First define your cloud data, using `text` and `size` properties:
//https://jsfiddle.net/plantface/g6faeurj/

// Next you need to use the layout script to calculate the placement, rotation and size of each word:

var width = 1000;
var height = 600;
var fill = d3.scaleOrdinal().domain([1,3]).range(["rgb(169,169,169)","rgb(69,173,168)","rgb(217,91,67)"]);

//reference : https://stackoverflow.com/questions/27672989/dynamically-sized-word-cloud-using-d3-cloud
var minFont = 1;
var maxFont = 20;
var fontSizeScale = d3.scalePow().exponent(5).domain([0,1]).range([ minFont, maxFont]);

//var maxSize = d3.max(wegmans_tweets_words_data, function (d) {return .info.M.word_count.N;});


//get color
function colorDimScale(sentiment)
{
	if (sentiment == "POSITIVE")
	{
		return fill(3);
	}
	else if (sentiment == "NEGATIVE") {
		return fill(2);
	}
	else {
		return fill(1);
	}
}


var maxSize = d3.max(wegmans_tweets_words_data, function (d) {return d.info.M.word_count.N;});

    d3.layout.cloud()
    	.size([width, height])
    	.words(wegmans_tweets_words_data)
    	.rotate(function() {
    		return 0;
    	})
    	.font("Impact")
    	.fontSize(function(d) { return d.info.M.word_count.N*3;})
      //.fontSize(function (d) { return fontSizeScale(d.info.M.word_count.N/maxSize);})
    	.on("end", drawSkillCloud)
    	.start();

// Finally implement `drawSkillCloud`, which performs the D3 drawing:

    // apply D3.js drawing API
    function drawSkillCloud(words) {
    	d3.select("#cloud").append("svg")
    		.attr("width", width)
    		.attr("height", height)
    		.append("g")
    		.attr("transform", "translate(" + ~~(width / 2) + "," + ~~(height / 2) + ")")
    		.selectAll("text")
    		.data(words)
    		.enter().append("text")
    		.style("font-size", function(d) {
          return (d.info.M.word_count.N)/3   + "vh";
    		})
    		.style("-webkit-touch-callout", "none")
    		.style("-webkit-user-select", "none")
    		.style("-khtml-user-select", "none")
    		.style("-moz-user-select", "none")
    		.style("-ms-user-select", "none")
    		.style("user-select", "none")
    		.style("cursor", "default")
    		.style("font-family", "Impact")
    		.style("fill", function(d, i ) { return colorDimScale(d.sentiment_type.S); })
    		.attr("text-anchor", "middle")
    		.attr("transform", function(d) {
    			return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    		})
    		.text(function(d) {
    			return d.word.S;
    		});
    }

// set the viewbox to content bounding box (zooming in on the content, effectively trimming whitespace)

    var svg = document.getElementsByTagName("svg")[0];
    var bbox = svg.getBBox();
    var viewBox = [bbox.x, bbox.y, bbox.width, bbox.height].join(" ");
    //var viewBox = ["1000", "1000", "1000", "1000"].join(" ");
    svg.setAttribute("viewBox", viewBox);
