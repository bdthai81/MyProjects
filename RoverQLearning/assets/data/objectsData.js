// rover object's dictionary of parameters
var roverData = {
    bodyWidth: 25,  // 25cm  width
    bodyHeight: 50, // 50cm length
    wheelAmount: 6, //best with even number
    wheelYPos: 20,
    wheelWidth: 2, //make sure to update objects.css to align with stroke-width
    wheelHeight: 5,
    // array list of the sensors' [angle,x,y] pixel position to rover's physical position
    sensors: [[-90, 2, 10], [-45, 5.25, 5], [0, 12.5, 0], [45, 17.75, 5], [90, 23, 10]], 
    sensorRange: 200 // reliable reading max range 200cm
  };

/**
 * Used testCollision.html to verify shapes and sizes
 * Used link below to gather coords for path
 * https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php
 * variable dictionary keys: imgName, width, height, path
 */

var cardinal = d3.svg.line()
    .interpolate("cardinal");

/**
 * Small Boulder: 14 coordinates
 * Image width = 75 px
 * Image height = 68 px
 */
var smallBoulderData = {
        imgName: "small_boulder",
        width: 75,
        height: 68,
        path: [[6,4], [15,1], [45,4], [73,16], [73,31],
               [71,44], [74,51], [72,66], [20,64], [13,67],
               [2,55], [6,38], [15,36], [6,4]]
    };

/**
 * Medium Boulder: 15 coordinates
 * Image width = 125 px
 * Image height = 111 px
 */
var mediumBoulderData = {
        imgName: "medium_boulder",
        width: 125,
        height: 111,
        path: [[7,38], [47,30], [54,7], [89,6], [101,41],
               [121,60], [122,73], [67,87], [63,100], [22,109],
               [5,100], [6,91], [18,78], [1,56], [7,38]]
    };

/**
 * Large Boulder: 27 coordinates
 * Image width = 200 px
 * Image height = 158 px
 */
var largeBoulderData = {
        imgName: "large_boulder",
        width: 200,
        height: 158,
        path: [[147,140], [197,142], [196,108], [180,95], [172,85],
               [157,81], [150,57], [117,59], [100,4], [88,2],
               [52,38], [47,84], [31,97], [21,113], [3,117],
               [1,129], [17,135], [33,128], [54,136], [79,130],
               [101,138], [96,146], [109,152], [118,148], [130,156],
               [151,152],[147,140]]
    };

/**
 * Pothole 1: 13 coordinates
 * Image width = 100 px
 * Image height = 46 px
 */
var pothole1Data = {
        imgName: "pothole1",
        width: 100,
        height: 46,
        path: [[4,36], [3,21], [17,6], [36,1], [64,1],
               [73,4], [93,18], [98,28], [76,32], [69,36],
               [51,39], [22,43], [4,36]]
    };

/**
 * Pothole 2: 12 coordinates
 * Image width = 100 px
 * Image height = 58 px
 */
var pothole2Data = {
        imgName: "pothole2",
        width: 100,
        height: 58,
        path: [[5,57], [5,48], [13,37], [25,16], [53,3],
               [76,3], [61,15], [98,26], [63,42], [47,38],
               [46,45], [5,57]]
    };

/**
 * Green mineral: 10 coordinates
 * Image width = 50 px
 * Image height = 38 px
 */
var greenMineralData = {
        imgName: "green_mineral",
        width: 50,
        height: 38,
        path: [[20,34], [8,37], [8,25], [2,8], [16,2],
               [24,8], [46,17], [50,26], [41,36], [20,34]]
    };

/**
 * Pink mineral: 13 coordinates
 * Image width = 31 px
 * Image height = 50 px
 */
var pinkMineralData = {
        imgName: "pink_mineral",
        width: 31,
        height: 50, 
        path: [[10,45], [10,39], [1,25], [4,18], [4,9],
               [5,3], [15,2], [29,11], [28,39], [30,44],
               [24,50], [17,47], [10,45]]
    };

/**
 * Blue mineral: 8 coordinates
 * Image width = 50 px
 * Image height = 37 px
 */
var blueMineralData = {
        imgName: "blue_mineral",
        width: 50,
        height: 37, 
        path: [[3,16], [12,3], [32,2], [47,12], [50,31],
               [29,36], [14,32], [3,16]]
    };
