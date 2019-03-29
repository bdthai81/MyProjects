/**
 * Shuffles array in place.
 * @param {Array} a items An array containing the items.
 */
function shuffle(a) {
  var j, x, i;
  for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      x = a[i];
      a[i] = a[j];
      a[j] = x;
  }
  return a;
}

/**
 * Global Variables
 */
// make a map of the student list to reference by index when plotting
var studentMap = studentList.map(d=>d);
// Concat the arrays of former groups into 1
var groupExisted = groupProject1.concat(groupProject2);
// Split the students into the following # of teams
var numTeams = 5;
// Number of Projects
var numProjects = 3;
// Set the number of max members in the team
var maxMembers = Math.ceil(studentList.length / numTeams);
// Reference student's former teammates
var studentDict = {}
// Keep track of shuffling for new teams to meet criteria
var shuffleCounter = 0;
// Array of new teams generated in function initNewTeamsData
var teams = [];

/*** Generate new teams data ***/
/** 
 * Function to load student dictionary of former teammates
 * key: student
 * value: array of former teammates
 */
function loadStudentDict() {
  studentList.forEach(student => {
    // Initialize student key with itself as the first element in the list
    studentDict[student] = [student];
    groupExisted.forEach(group => {
      //student exists in group. append former members into student dictionary
      if(group.indexOf(student) !== -1) {
        studentDict[student] = studentDict[student].concat(group.filter(members => members !== student));
      }
    })
  });
}

/**
 * function shuffle new teams: generates a multiple array of new teams
 * that consists of members collaborating for the first time in projects.
 * 
 * returns multiple array of new teams
 */
function shuffleNewTeams() {
  // array of new teams
  var teams = [];
  // Shuffle new random teams
  for(i=0; i<numTeams; i++) {
    // shuffle the array of students remaining
    studentList = shuffle(studentList);
    // Take last student on studentList and initial a new team array as the first member
    var newMember = studentList.pop(); 
    var newTeam = [newMember];
    // update studentList by removing the new member
    // newMembers: filter an array of students that haven't teamup with the newMember before
    var newMembers = studentList.filter(e => studentDict[newMember].indexOf(e) === -1);
    // Add the rest of the new team's members
    for(j=1; j<maxMembers; j++ ) {
      // Shuffle the newMembers potential list and pop the next new Member
      newMember = shuffle(newMembers).pop();
      // Add new member into newTeam
      newTeam.push(newMember);
      // update newMembers by filtering out newMembers' old teammates
      newMembers = newMembers.filter(e => studentDict[newMember].indexOf(e) === -1);
    }
    // break off shuffle, not enough new members to fulfill this team
    if(newTeam.filter(e => e !== undefined).length < maxMembers) {
      console.log("break");
      break;
    };
    // Push new team in the array of teams
    teams.push(newTeam);
    // Update studentList by filtering out new team members from array
    studentList = studentList.filter(e => newTeam.indexOf(e) === -1);
    // Update maxMembers so the top teams get the larger team and balance out the team amount
    maxMembers = Math.ceil(studentList.length / (numTeams-(i+1)));
    console.log(i + " " + studentList.length + " " + maxMembers);
  }
  // return multiple array of new teams
  return teams;
}

/**
 * function to initialize the new Teams
 */
function initNewTeamsData() {
  // execute load student dictionary
  loadStudentDict();

  // initialize a list of new teams
  shuffleCounter = 1;
  teams = shuffleNewTeams();
  // flatten new teams multi-array to verify for any undefined
  var flattenTeams = [].concat.apply([], teams);
  // filter out undefined 
  flattenTeams = flattenTeams.filter(e => e !== undefined)
  console.log(flattenTeams.length);
  // Reshuffle if all students are not assigned
  while((flattenTeams.length !== studentMap.length)) {
    // Reset studentList
    studentList = studentMap.map(d=>d);
    // Reshuffle new teams
    teams = shuffleNewTeams();
    // flatten new teams multi-array to verify for any undefined
    flattenTeams = [].concat.apply([], teams);
    // filter out undefined 
    flattenTeams = flattenTeams.filter(e => e !== undefined)
    // increment counter
    shuffleCounter = shuffleCounter + 1;
  }
  // Print counter and teams in console
  console.log("shuffle counter:" + shuffleCounter);
  console.log(teams);
}

// Run initNewTeamsData & load and generate new teams data
initNewTeamsData();

/**
 * Generate Chart
 */
// Set canvas width and heigth of chart & margins
var svgWidth = 700;
var svgHeight = 700;

var margin = {
  top: 40,
  right: 40,
  bottom: 40,
  left: 40
};

var chartWidth = svgWidth - margin.left - margin.right;
var chartHeight = svgHeight - margin.top - margin.bottom;

// colors for circles by index
var colors = d3.scaleQuantize()
  .domain([0,studentMap.length])
  .range(["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf","#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928","#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#ffff33","#a65628","#f781bf","#999999"]);


// Create an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
var svg = d3
  .select("#chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append an SVG group
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// scale y to chart height
var yScale = d3.scaleLinear()
  .domain([-0.5, (studentMap.length-1)+0.5])
  .range([chartHeight, 0]);

// scale x to chart width
var xScale = d3.scaleLinear()
  .domain([-0.1, 3.1])
  .range([0, chartWidth]);

// create axes
var yAxis = d3.axisLeft(yScale)
  .ticks(studentMap.length)
  .tickFormat(d => studentMap[d]);
var xAxis = d3.axisBottom(xScale);

// set x to the bottom of the chart
chartGroup.append("g")
  .attr("transform", `translate(0, ${chartHeight})`)
  .call(xAxis);

// set y to the y axis
chartGroup.append("g")
  .call(yAxis);

// return the new team # the member is in
function getNewTeam(member) {
  var newTeam = null;
  teams.forEach((team, ix) => {
    if(team.indexOf(member) !== -1) {
      newTeam = ix;
    };
  });

  return newTeam;
}

/**
 * function activates the links based on the hover selected member
 * @param {*} selectedMember : user hover over member circle tag
 */
function activateLinks(selectedMember) {
  // Load all links
  var selectedLinks = d3.selectAll(".link");

  if(selectedMember === "all") {
    // activate all links
    selectedLinks.classed("invisible", false);
    d3.selectAll(`[value=invisble]`).classed("invisible", true);
  }
  else {
    // inactivate all links
    selectedLinks.classed("invisible", true);
    // hide invisibles links to self
    d3.selectAll(`[value=invisble]`).classed("invisible", true);
    // activate selectedMember's links
    d3.selectAll(`[value=member${selectedMember}]`).classed("invisible", false);
  }
}

/**
 * function used for updating circles group with new tooltip
 * @param {*} circleEnter: Circle Tag to append Tooltip
 */
function updateToolTip(circleEnter) {
  // Setup the tool tip.  Note that this is just one example, and that many styling options are available.
  // See original documentation for more details on styling: http://labratrevenge.com/d3-tip/
  var tool_tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([-8, 0])
      .html(d => `${d}<br>Team Members: ${teams[getNewTeam(d)].filter(e=>e!==d)}<br>Former members: ${studentDict[d].filter(e=>e!==d)}`);
  
  svg.call(tool_tip);

  // Assign hover events
  circleEnter.classed("active inactive", true)
  .on('mouseover', tool_tip.show)
  .on('mouseout', tool_tip.hide)
  .on('mouseenter', function() {
      // activate links based on selected member's circle
      activateLinks(d3.select(this).attr("value"));
  })
  .on('mouseleave', function() {
      // activate all links
      activateLinks("all");
  });
}

/**
 * function creates a Group of circles based on Project # (x-axis)
 * @param {*} chartGroup : group tag that embeds all the members' circle tag
 * @param {*} projectNumber : Project # the circle tags belong to
 */
function createGroupProject(chartGroup, projectNumber) {

  // add circle for each student in project
  projectGroup = chartGroup.append("g")
    .attr("id", "project" + projectNumber);
  // data bind the students
  var circleGroup = projectGroup.selectAll("circle")
    .data(studentMap);
  // append the circle tags
  var circleEnter = circleGroup.enter()
    .append("circle")
    .attr("cx", xScale(projectNumber))
    .attr("cy", (d,i) => yScale(i))
    .attr("r", 10)
    .attr("fill", (d,i) => colors(i))
    .attr("value", (d,i) => i);

  // update Tooltips to the circles
  updateToolTip(circleEnter);
}

/**
 * function create the links between team members based on project
 * @param {*} projectData : data for members of each team in the project
 * @param {*} linkProjects : group tag to append the link tags to
 * @param {*} projectNumber : project number
 */
function createLinksProject(projectData, linkProjects, projectNumber) {
  // draw links per team
  projectData.forEach((team, teamIx) => {
    // draw links per member
    team.forEach(member => {
      var linkTeams = linkProjects.append("g")
        .attr("id", "linkTeam" + teamIx);
      linkTeams.selectAll("line")
      .data(team)
      .enter().append("line")
      .classed("link", true)
      .classed("invisible", d => (d===member) ? true:false)
      .attr("value", d => (d===member) ? "invisble":"member"+studentMap.indexOf(d))
      .attr("x1", xScale(projectNumber-1))
      .attr("y1", yScale(studentMap.indexOf(member)))
      .attr("x2", xScale(projectNumber))
      .attr("y2", d => yScale(studentMap.indexOf(d)));
    });
  });
}

/**
 * Function to initialize the chart
 */
function initChart() {
  
  // Draw Links for Project 1
  var projectNumber = 1;
  // add link for each team member in project
  var linkProjects = chartGroup.append("g")
    .attr("id", "linkProject" + projectNumber);
  // Create links between teammates in project 1
  createLinksProject(groupProject1, linkProjects, projectNumber);

  // Draw Links for Project 2
  projectNumber = 2;
  // add link for each team member in project
  linkProjects = chartGroup.append("g")
    .attr("id", "linkProject" + projectNumber);
  // Create links between teammates in project 2
  createLinksProject(groupProject2, linkProjects, projectNumber);
  
  // Draw Links for Project 3
  projectNumber = 3;
  // add link for each team member in project
  var linkProjects = chartGroup.append("g")
    .attr("id", "linkProject" + projectNumber);
  // Create links between teammates in project 3
  createLinksProject(teams, linkProjects, projectNumber);

  // Create student circles for all the projects
  for(i=0; i<(numProjects+1); i++) {
    createGroupProject(chartGroup, i)
  }

  // Declare display string
  var display = ``
  // Append teams to display
  teams.forEach((team, ix) => {
    display = display + `Team ${ix+1}: ${team}<br>`
  });
  // Append Shuffle count to display string
  display = display + `<br><h6>Shuffle count: ${shuffleCounter}</h6>`;
  // render display in html
  d3.select("#displayNewTeams").html(display);
}

// Execute initChar()
initChart();
