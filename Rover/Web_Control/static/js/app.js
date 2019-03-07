// Create SVG button
function createSVGBtn(name, size, x, y, rotateAngle) {
    var init_xy = 10; // path started at (10,10) 
    id = name.replace(/[ .]/g, "_");

    d3.select('#' + id).append("use")
              .attr("id", name)
              .attr("xlink:href", size)
              .attr("x", x)
              .attr("y", y)
              .attr("transform", "rotate(" + rotateAngle + " " + (x+init_xy) + " " + (y+init_xy) + ")");
};

// Create Text
function createSVGText(name, x, y) {
    id = name.replace(/[ .]/g, "_");

    d3.select('#' + id).append("text")
              .attr("x", x)
              .attr("y", y)
              .attr("fill", "white")
              .text(name);
};

// Create Text with rotation
function createSVGText(name, x, y, transform) {
    id = name.replace(/[ .]/g, "_");

    d3.select('#' + id).append("text")
              .attr("x", x)
              .attr("y", y)
              .attr("fill", "white")
              .text(name)
              .attr("transform", transform);
};

// Initialize SVG Web Control buttons
function init() {
    var zero_xy = -10; // Reset svg to (0,0) x,y point; 
    var md_padding = 20; // Same as the stroke-width
    var lg_padding = 15;
    var mid_point_xy = 180; // Center of svg(360,360)
    var md_length = 50; // Triangle large's a,b length 
    var lg_length = 100; // Triangle large's a,b length 
    var hypotenuse_md = Math.sqrt((md_length**2)*2) ;

    var shift_a = zero_xy + mid_point_xy - (hypotenuse_md/2);
    var shift_b = zero_xy + mid_point_xy + (hypotenuse_md/2);
    // Add left, forward, right, down buttons
    createSVGBtn("Left", "#triangle_md", shift_a - md_padding, shift_a, "45");
    createSVGBtn("Forward", "#triangle_md", shift_b, shift_a - md_padding, "135");
    createSVGBtn("Right", "#triangle_md", shift_b + md_padding, shift_b, "225");
    createSVGBtn("Reverse", "#triangle_md", shift_a, shift_b + md_padding, "315");
    // Add pivot left, right buttons
    shift_a = zero_xy + mid_point_xy - lg_length - lg_padding;
    shift_b = zero_xy + mid_point_xy + lg_padding;
    createSVGBtn("Pivot Left", "#triangle_lg", shift_a, shift_b, "0");
    shift_a = zero_xy + mid_point_xy + lg_length + lg_padding;
    createSVGBtn("Pivot Right", "#triangle_lg", shift_b, shift_a, "270");
    // Add camera tilt left, right, up, down buttons
    shift_a = zero_xy + mid_point_xy - lg_length - (md_padding/2);
    shift_b = zero_xy + mid_point_xy - md_padding;
    createSVGBtn("T.L.", "#triangle_md", shift_a, shift_b, "-135");
    shift_b = zero_xy + mid_point_xy + md_padding;
    createSVGBtn("T.D.", "#triangle_md", shift_b, shift_a, "-45");
    shift_b = zero_xy + mid_point_xy - lg_length + (md_padding/2);
    createSVGBtn("T.U.", "#triangle_md", shift_b, shift_a, "-45");
    shift_a = zero_xy + mid_point_xy + lg_length + (md_padding/2);
    createSVGBtn("T.R.", "#triangle_md", shift_a, shift_b, "45");

    // Add Web Control Text labels for button
    createSVGText("Forward", "150", "125");
    createSVGText("Reverse", "152", "248");
    createSVGText("Left", "97", "184");
    createSVGText("Right", "233", "184");
    createSVGText("Pivot Left", "85", "235", "rotate(45 85 235)");
    createSVGText("Pivot Right", "230", "280", "rotate(-45 230 280)");
    createSVGText("T.U.", "111", "88");
    createSVGText("T.D.", "222", "88");
    createSVGText("T.L.", "71", "129");
    createSVGText("T.R.", "265", "129");
};

// Run init()
init()

// Declare SVG Control Buttons & Event Handler
d3.selectAll("g").on("mousedown", function() {
    // you can select the element just like any other selection
    var gBtn = d3.select(this);
    
    var web_json = { "webCommand": gBtn.attr("id") };
    
    // ajax the JSON to the server: start motion
    $.ajax({
        type: 'POST',
        url: '/command',
        data: JSON.stringify (web_json),
        success: function(data) { },
        contentType: "application/json",
        dataType: 'json'
    });
});

d3.selectAll("g").on("mouseup", function() {
    // ajax the JSON to the server: stop_motion
    $.ajax({
        type: 'POST',
        url: '/stop_motion',
        data: JSON.stringify (""),
        success: function(data) { },
        contentType: "application/json",
        dataType: 'text'
    });
});

// stream images
var boolFPS = false;

function image_action() {
    var curRoverViewImg = "./static/images/rover_view/rover_view_" + new Date().getTime() + ".png";
    var img_json = { "imgName": curRoverViewImg };
    // ajax the JSON to the server to start motion
    $.ajax({
        type: 'POST',
        url: '/camera_image',
        data: JSON.stringify (img_json),
        success: function(data) { 
            // refresh rover image
            d3.select("#rover_view_img").attr("src", curRoverViewImg);
        },
        contentType: "application/json",
        dataType: 'text'
    });
    
};

d3.select("#btnRView").on("click", function() {
    boolFPS = !boolFPS;
    //update btn display to enabled
    d3.select("#btnRView").text("Enabled");
    
    if (boolFPS) {
        image_action();
        // execute action every 1.5seconds
        timer = setInterval(image_action, 1500);
    }
    else {
        clearInterval(timer);
        //update btn display to disabled
        d3.select("#btnRView").text("Disabled");
    }
    
});
  
