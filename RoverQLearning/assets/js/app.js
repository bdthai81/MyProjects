// Define SVG area dimensions
var svgWidth = 960;
var svgHeight = 720;

// Define the window's margins as an object
var windowMargin = {
  top: 5,
  right: 5,
  bottom: 5,
  left: 5
};

// Define dimensions of the window area
var windowWidth = svgWidth - windowMargin.left - windowMargin.right;
var windowHeight = svgHeight - windowMargin.top - windowMargin.bottom;

// Select body, append SVG area to it, and set the dimensions
var svg = d3.select("#window")
  .append("svg")
  .attr("height", svgHeight)
  .attr("width", svgWidth);

// Create landscape
var landscape = svg.append("svg:image")
  .attr("width", "100%")
  .attr("height", "100%")
  .attr("xlink:href", "./assets/images/landscape.png");

// Create rover object
var rover = createRover(svg);

// Declare object array to store all the block/mineral objects' dimensions
var objectsList = [];
// Create mineral deposit objects
var gObj = svg.append("g").attr("id", blueMineralData.imgName);
var blueMineral = createObject(gObj, blueMineralData, 525, 125, objectsList);
gObj = svg.append("g").attr("id", greenMineralData.imgName);
var greenMineral = createObject(gObj, greenMineralData, 25, 25, objectsList);
gObj = svg.append("g").attr("id", pinkMineralData.imgName);
var pinkMineral = createObject(gObj, pinkMineralData, 25, 525, objectsList);

// Create boulder objects
gObj = svg.append("g").attr("id", smallBoulderData.imgName);
var smallBoulder = createObject(gObj, smallBoulderData, 225, 375,objectsList);
gObj = svg.append("g").attr("id", mediumBoulderData.imgName);
var mediumBoulder = createObject(gObj, mediumBoulderData, 450, 15, objectsList);
gObj = svg.append("g").attr("id", largeBoulderData.imgName);
var largeBoulder = createObject(gObj, largeBoulderData, 325, 500, objectsList);
console.log(objectsList);


// rover's position point [rotate, x, y]
var point = [0, svgWidth/2, svgHeight/2];
// log of rover's movement
var momentum = [0, 0];

// Create 5 sensor line/circle
roverData.sensors.forEach(sensor => {
  var gSensor = svg.append("g")
    .attr("id", `sensor${sensor[0]}`);
  gSensor.append("line");
  gSensor.append("circle")
    .attr("cx", -10)
    .attr("cy", -10)
    .attr("r", 3.5);
  gSensor.append("text");
});

function move(distance) {
  // move rotate a positive angle
  point[0] = (point[0]+360)%360;
  // Rotate momentum's position based on angle
  var m  = rotate(momentum[0], momentum[1], momentum[0], momentum[1]+distance, point[0]);

  return [momentum[0] + m.x, momentum[1] + m.y]
}

function motion(command) {
  return function(event) {
    // Prevent refresh
    event.preventDefault();
    // execute command
    switch(command) {
      case "Forward":
        // Update movement
        momentum = move(-1);
        break;
      case "Reverse":
        // Update movement
        momentum = move(1);
        break;
      case "Pivot_Left":
        // Update movement
        point[0] -= 15;
        break;
      case "Pivot_Right":
        // Update movement
        point[0] += 15;
        break;
      default:
        console.log("Unknown command");
    }
  };
}

d3.select('body').call(d3.keybinding()
  .on('←', motion("Pivot_Left"))
  .on('↑', motion("Forward"))
  .on('→', motion("Pivot_Right"))
  .on('↓', motion("Reverse")));

d3.timer(function() {
  // Keep rover's position within the window
  point[1] = Math.min(svgWidth,  Math.max(0, momentum[0] + point[1]));
  point[2] = Math.min(svgHeight, Math.max(0, momentum[1] + point[2]));

  // Update rover's position
  rover
    .datum(point)
    // rotate rover by user input, translate by user input, translate set rover point to center of the body
    .attr('transform', d => `rotate(${d}) translate(${d[1]} ${d[2]}) translate(${-roverData.bodyWidth/2} ${-roverData.bodyHeight/2})`);
  momentum[0] *= 0.9;
  momentum[1] *= 0.9;

  // Update all 5 sensors
  roverData.sensors.forEach(sensor => {
    // Get each sensor's angle position & add to rover's current angle position
    var angle = sensor[0] + point[0];
     // Check objects list for any objects within max range of sensor
    var p = sensorDistance(angle, point[1], point[2], objectsList);
    // Update sensor's x,y after rover rotation
    var m = rotate(point[1], point[2], point[1]-(roverData.bodyWidth/2)+sensor[1], point[2]-(roverData.bodyHeight/2)+sensor[2], point[0]);

    if(p) {
      // Object detected within sensor's range
      var gSensor = d3.select(`#sensor${sensor[0]}`);
      // Display range
      gSensor.select("line").attr("x1", p.x).attr("y1", p.y).attr("x2", m.x).attr("y2", m.y).style("opacity", .8);
      gSensor.select("circle").attr("cx", p.x).attr("cy", p.y).style("opacity", .8);
      gSensor.select("text").attr("x", p.x).attr("y", p.y).text(p.distance).style("opacity", .8);
    }
    else {
      // no object within range, disable display
      var gSensor = d3.select(`#sensor${sensor[0]}`);
      gSensor.select("line").style("opacity", 0);
      gSensor.select("circle").style("opacity", 0);
      gSensor.select("text").style("opacity", 0);
    }
  })
});

// Scan and return distance on sensor from objects within max range
function sensorDistance(angle, x, y, objectsList) {
  var p = null;
  var maxDistance = roverData.sensorRange;
  // Check to see if any objects are within the sensor's range
  objectsList.forEach(e => {
    // Create Rectangle within object's -45 range
    var avgX = ((e.xMin+e.xMax)/2);
    var avgY = ((e.yMin+e.yMax)/2);
    var cx = avgX;
    var cy = avgY;
    var sbw = smallBoulderData.width/2;
    var sbh = smallBoulderData.height/2;
    var r = {
      A: rotate(cx, cy, avgX-sbw, cy+sbh, angle),
      B: rotate(cx, cy, cx+sbw, cy+sbh, angle),
      C: rotate(cx, cy, cx+sbw, cy+sbh+maxDistance, angle),
      D: rotate(cx, cy, cx-sbw, cy+sbh+maxDistance, angle)
    }
    // Create m point from x,y
    var m = {x: x, y: y};
    //  console.log(e.name, r);
    // Check if point is in rectangle (object's sensor range)
    if(pointInRectangle(m, r))  {
      var objDetected = d3.select(`#${e.name} path`);
      p = closestPoint(objDetected.node(), m);
    } 
  });

  return p;
}


