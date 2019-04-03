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

var line = svg.append("line");

var circle = svg.append("circle")
    .attr("cx", -10)
    .attr("cy", -10)
    .attr("r", 3.5);

var text = svg.append("text")
    .attr("id", "distance")
    .attr("x", 150)
    .attr("y", 20)
    .text("distance: ");

// rover's position point [rotate, x, y]
var point = [0, svgWidth/2, svgHeight/2];
// log of rover's movement
var momentum = [0, 0];

function move(distance) {
  // move rotate a positive angle
  point[0] = (point[0]+360)%360;
  // move based on rotate angle
  switch(point[0]) {
    case 0:
      return [momentum[0], momentum[1] - distance];
    case 90:
      return [momentum[0] + distance, momentum[1]];
    case 180:
      return [momentum[0], momentum[1] + distance];
    case 270:
      return [momentum[0] - distance, momentum[1]];
  }
  return [momentum[0], momentum[1]]
}

function motion(command) {
  return function(event) {
    // Prevent refresh
    event.preventDefault();
    // execute command
    switch(command) {
      case "Forward":
        // Update movement
        momentum = move(2);
        break;
      case "Reverse":
        // Update movement
        momentum = move(-2);
        break;
      case "Pivot_Left":
        // Update movement
        point[0] -= 90;
        break;
      case "Pivot_Right":
        // Update movement
        point[0] += 90;
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

  // Update sensors
  var p = sensorDistance(-45, point[1], point[2], objectsList);
  var m = {x: point[1], y: point[2]};
  console.log(p);
  if(p) {
    line.attr("x1", p.x).attr("y1", p.y).attr("x2", m.x).attr("y2", m.y);
    circle.attr("cx", p.x).attr("cy", p.y);
    text.text("distance: " + p.distance);

    // console.log(m, p);
  }
});

// Scan and return distance on sensor from objects within max range
function sensorDistance(angle, x, y, objectsList) {
  var p = null
  var maxDistance = roverData.sensorRange;
  var distance = roverData.sensorRange;
  // Check to see if any objects are within the sensor's range
  objectsList.forEach(e => {
    
    // sensor0 left view
    if((angle===-90)&&(y>e.yMin) && (y<e.yMax) && ((x-e.xMax)>0) && ((x-e.xMax)<maxDistance)) {
      // update closest object
      if(distance > (x-e.xMax)) {
        distance = (x-e.xMax);
        var objDetected = d3.select(`#${e.name} path`);
      }
    }
    // sensor1 left-front view
    if(angle==-45) {
      // Create Rectangle within object's -45 range
      var r = {
        A: {x: e.xMin, y: e.yMax},
        B: {x: e.xMax, y: e.yMin},
        C: {x: e.xMin+maxDistance, y: e.yMax+maxDistance},
        D: {x: e.xMax+maxDistance, y: e.yMin+maxDistance}
      }
      // Create m point from x,y
      var m = {x: x, y: y};
      // Check if point is in rectangle (object's sensor range)
      if(pointInRectangle(m, r))  {
        var objDetected = d3.select(`#${e.name} path`);
        console.log(objDetected);
        p = closestPoint(objDetected.node(), m);
      }
    }
    
    // sensor2 front view 
    // check if conditions met: obj.xMin < x < obj.xMax && 0 < (y-yMax) < maxRange
    // for object detection within max range of snesor
    if((angle===0)&&(x>e.xMin) && (x<e.xMax) && ((y-e.yMax)>0) && ((y-e.yMax)<maxDistance)) {
      // update closest object
      if(distance > (y-e.yMax)) {
        distance = (y-e.yMax);
        var objDetected = d3.select(`#${e.name} path`);
      }
    }
    
    // sensor3 right-front view
    // sensor4 right view
    if((angle===90)&&(y>e.yMin) && (y<e.yMax) && ((e.xMax-x)>0) && ((e.xMax-x)<maxDistance)) {
      // update closest object
      if(distance > (x-e.xMax)) {
        distance = (x-e.xMax);
        var objDetected = d3.select(`#${e.name} path`);
      }
    }
  });

  return p;
}


