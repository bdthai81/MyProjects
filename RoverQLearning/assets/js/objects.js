/**
 * Objects: rover, block, minerals
 */

/**
 * Function creates the rover object: 1px = 1cm scale
 * @param {*} parentNode: D3 parent node element to append the rover object
 * return rover object
 */
function createRover(parentNode) {
  
  // Create group tag for rover's id & position
  var rover = parentNode.append("g")
      .attr("id", "rover")
      .classed("rover", true);
      // .attr("transform", `translate(${roverObject.xPos}, ${roverObject.yPos})`);
    
  // Create rover's body
  rover.append("rect")
    .attr("x", roverData.wheelWidth)
    .attr("width", roverData.bodyWidth-(roverData.wheelWidth*2)) // substract 4px for wheels
    .attr("height", roverData.bodyHeight);
  // Create rover's wheels
  for(i=0; i<roverData.wheelAmount; i++) {
    if((i%2)===0) {
      // Create left axis wheel
      rover.append("line")
        .attr("y1", roverData.wheelYPos+(roverData.wheelHeight*i))
        .attr("y2", roverData.wheelYPos+(roverData.wheelHeight*i)+roverData.wheelHeight)
    }
    else {
      // Create right axis wheel
      rover.append("line")
        .attr("x1", roverData.bodyWidth)
        .attr("y1", roverData.wheelYPos+(roverData.wheelHeight*(i-1)))
        .attr("x2", roverData.bodyWidth)
        .attr("y2", roverData.wheelYPos+(roverData.wheelHeight*(i-1))+roverData.wheelHeight)
    };
  };
  
  // Create rover's camera
  rover.append("path")
    .attr("id", "camera")
    .attr("d", "M7.5 10 L17.5 10 L12.5 17 Z");
  
  // Create Sensors' sonar scan
  roverData.sensors.forEach((sensor, ix) => {
    rover.append("path")
      .attr("id", "sensor"+ix)
      .classed("sensor", true)
      .attr("d", `M${sensor[1]} ${sensor[2]} ${sensor[1]} ${-roverData.sensorRange}`)
      .attr("transform", `rotate(${sensor[0]} ${sensor[1]} ${sensor[2]})`);
  });

  return rover;
}

/**
 * Function creates a block/mineral object: 1px = 1cm scale
 * @param {*} parentNode: D3 parent node element to append the block/mineral object
 * @param {*} obj: object's dictionary variables from objectsData.js
 * @param {*} x: x position 
 * @param {*} y: y position
 * @param {*} ol: (objectsList) add array of the object's dimensions into ol
 * return block/mineral object
 */
function createObject(parentNode, obj, x, y, ol) {
  // Align path to x,y
  obj.path.forEach(function (element) {
    element[0] += x;
    element[1] += y;
  })
  // Create definition for object's pattern image
  var patternID = obj.imgName + "Pattern";
  parentNode.append('pattern')
    .attr('id', patternID)
    .attr('patternUnits', 'userSpaceOnUse')
    .attr('width', obj.width)
    .attr('height', obj.height)
    .attr("x", x)
    .attr("y", y)
    .append("image")
    .attr("xlink:href", `./assets/images/${obj.imgName}.png`)
    .attr('width', obj.width)
    .attr('height', obj.height);
  // Create object path
  var object = parentNode.append("path")
    .datum(obj.path)
    .attr("d", cardinal)
    .style("stroke", "blue")
    .style("stroke-width", 0)
    .style("fill", `url(#${patternID})`);
  // Add dictionary dimensions & path into ol array
  var objDimesions = {
    name: obj.imgName,
    xMin: d3.min(obj.path, d => d[0]),
    xMax: d3.max(obj.path, d => d[0]),
    yMin: d3.min(obj.path, d => d[1]),
    yMax: d3.max(obj.path, d => d[1])
  };
  ol.push(objDimesions);

  return object;
}
