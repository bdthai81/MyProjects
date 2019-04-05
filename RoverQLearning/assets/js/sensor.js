/**
 * Function finds the closest path between sensor and the block/mineral object
 * @param {*} pathNode : D3 path block/mineral object
 * @param {*} point : {x: x, y: y}
 * returns best point{x,y} and distance
 */
function closestPoint(pathNode, point) {
    var pathLength = pathNode.getTotalLength(),
        precision = 8,
        best,
        bestLength,
        bestDistance = Infinity;
    
    // linear scan for coarse approximation
    for (var scan, scanLength = 0, scanDistance; scanLength <= pathLength; scanLength += precision) {
      if ((scanDistance = distance2(scan = pathNode.getPointAtLength(scanLength))) < bestDistance) {
        best = scan, bestLength = scanLength, bestDistance = scanDistance;
      }
    }
  
    // binary search for precise estimate
    precision /= 2;
    while (precision > 0.5) {
      var before,
          after,
          beforeLength,
          afterLength,
          beforeDistance,
          afterDistance;
      if ((beforeLength = bestLength - precision) >= 0 && (beforeDistance = distance2(before = pathNode.getPointAtLength(beforeLength))) < bestDistance) {
        best = before, bestLength = beforeLength, bestDistance = beforeDistance;
      } else if ((afterLength = bestLength + precision) <= pathLength && (afterDistance = distance2(after = pathNode.getPointAtLength(afterLength))) < bestDistance) {
        best = after, bestLength = afterLength, bestDistance = afterDistance;
      } else {
        precision /= 2;
      }
    }
  
    // best = [best.x, best.y];
    best = {x: best.x, y: best.y};
    best.distance = Math.sqrt(bestDistance);
    return best;
  
    function distance2(p) {
      var dx = p.x - point.x,
          dy = p.y - point.y;
      return dx * dx + dy * dy;
    }
}


/**
 * Function rotates around the central point by the provided angle
 * @param {*} cx : Central point x (origin)
 * @param {*} cy : Central point y (origin)
 * @param {*} x : The x coordinate of the point that we'll be rotating
 * @param {*} y : The y coordinate of the point that we'll be rotating
 * @param {*} angle : The angle, in degrees.
 * returns the new x,y after rotation
 */
function rotate(cx, cy, x, y, angle) {
  var radians = -(Math.PI / 180) * angle,
      cos = Math.cos(radians),
      sin = Math.sin(radians),
      nx = (cos * (x - cx)) + (sin * (y - cy)) + cx,
      ny = (cos * (y - cy)) - (sin * (x - cx)) + cy;
  return {x: nx, y: ny};
}

/**
 * Rectangle is represented by points ABCD
 * Test if given point m is inside rectangle is given by:
 * 0 <= dot(AB,AM) <= dot(AB,AB) && 0 <= dot(BC,BM) <= dot(BC,BC)
 */

/**
 * Variable r stores the rectangle's 4 points: A,B,C,D
 * sample default values for -45 angle
 *
 *var r = {
 *    A: {x: 0, y: 100},
 *    B: {x: 100, y: 0},
 *    C: {x: 300, y: 200},
 *    D: {x: 200, y: 300}
 *    }
 */

/**
 * function checks point within the rectangle
 * @param {*} m : position of point to verify
 * @param {*} r : rectangles' 4 points
 * returns: true/false
 */

function pointInRectangle(m, r) {
    var AB = vector(r.A, r.B);
    var AM = vector(r.A, m);
    var BC = vector(r.B, r.C);
    var BM = vector(r.B, m);
    var dotABAM = dot(AB, AM);
    var dotABAB = dot(AB, AB);
    var dotBCBM = dot(BC, BM);
    var dotBCBC = dot(BC, BC);
    // console.log(AB, AM, BC, BM, dotABAM, dotABAB, dotBCBM, dotBCBC)
    return 0 <= dotABAM && dotABAM <= dotABAB && 0 <= dotBCBM && dotBCBM <= dotBCBC;
}
  
/**
 * function calculates the vector between two points
 * @param {*} p1 : point 1
 * @param {*} p2 : point 2
 * returns: vector result
 */
function vector(p1, p2) {
    return {
            x: (p2.x - p1.x),
            y: (p2.y - p1.y)
    };
}
  
/**
 * function calculates the dot product of two vectors
 * @param {*} u : vector 1
 * @param {*} v : vector 2
 * returns: dot product result
 */
function dot(u, v) {
    return u.x * v.x + u.y * v.y; 
}
